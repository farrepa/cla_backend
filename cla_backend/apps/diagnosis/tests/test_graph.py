from django.test import TestCase

from django.conf import settings
from django.core.management import call_command

from cla_common.constants import DIAGNOSIS_SCOPE, MATTER_TYPE_LEVELS

from legalaid.models import Category, MatterType

from diagnosis.graph import get_graph
from diagnosis.utils import get_node_scope_value

if not hasattr(settings, 'ORIGINAL_DIAGNOSIS_FILE_NAME'):
    raise Exception(
        'Please set ORIGINAL_DIAGNOSIS_FILE_NAME to the original path_file'
    )


class GraphTestCase(TestCase):

    def setUp(self):
        self.graph = get_graph(
            file_name=settings.ORIGINAL_DIAGNOSIS_FILE_NAME
        )
        self.checker_graph = get_graph(
            file_name=settings.ORIGINAL_CHECKER_DIAGNOSIS_FILE_NAME
        )
        call_command('loaddata', 'initial_category')
        call_command('loaddata', 'initial_mattertype')

    def assertCategoryInContext(self, context, nodes):
        # checking that the category is set and is valid
        category_name = context.get('category')
        try:
            return Category.objects.get(code=category_name)
            # GOOD
        except Category.DoesNotExist:
            self.assertTrue(False,
                'None of the nodes in this path (%s) have category set! Or the category doesn\'t match any record in the database (category: %s)' % (
                '\n'.join([node['label']+' '+node['id'] for node in nodes]), category_name
            ))

    def assertMatterTypesInContext(self, context, category, nodes):
        matter_type1_code = context.get('matter-type-1')
        matter_type2_code = context.get('matter-type-2')
        if matter_type2_code and not matter_type1_code:
            self.assertTrue(False,
                'MatterType2 (%s) set but MatterType1 == None for nodes in this path (%s)' % (
                    matter_type2_code,
                    '\n'.join([node['label']+' '+node['id'] for node in nodes])
                )
            )

        self.assertMatterType(matter_type1_code, MATTER_TYPE_LEVELS.ONE, category, nodes)
        self.assertMatterType(matter_type2_code, MATTER_TYPE_LEVELS.TWO, category, nodes)

    def assertMatterType(self, matter_type_code, level, category, nodes):
        if matter_type_code:
            # checking that matter type is valid
            try:
                return MatterType.objects.get(code=matter_type_code, level=level, category=category)
            except MatterType.DoesNotExist:
                self.assertTrue(False,
                    'MatterType (%s) for nodes in this path (%s) doesn\'t match any record in the database (level %s, category %s)' % (
                        matter_type_code,
                        '\n'.join([node['label']+' '+node['id'] for node in nodes]),
                        level, category.code
                ))

    def test_end_nodes_have_category(self):
        def move_down(node_id, context, nodes):
            node = self.graph.node[node_id]
            node['id'] = node_id

            nodes = list(nodes)
            nodes.append(node)

            context = dict(context)
            context.update(node['context'] or {})

            scope_value = get_node_scope_value(self.graph, node_id)
            if scope_value in [DIAGNOSIS_SCOPE.INSCOPE, DIAGNOSIS_SCOPE.OUTOFSCOPE]:
                category = self.assertCategoryInContext(context, nodes)
                self.assertMatterTypesInContext(context, category, nodes)

            for child_id in self.graph.successors(node_id):
                move_down(child_id, context, nodes)

        root_id = self.graph.graph['operator_root_id']
        move_down(root_id, {}, [])

        root_id = self.checker_graph.graph['operator_root_id']
        move_down(root_id, {}, [])

    def test_nodes_have_heading(self):
        checker_graph = get_graph(
            file_name=settings.CHECKER_DIAGNOSIS_FILE_NAME
        )
        node = checker_graph.node['n43::n2']
        self.assertEqual(node['heading'], u'Select the option that best describes your situation')
