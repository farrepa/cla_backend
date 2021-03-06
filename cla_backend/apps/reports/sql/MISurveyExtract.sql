SELECT
    md5(lower(regexp_replace((pd.full_name || pd.postcode) :: TEXT, '\s+', '', 'ig'))) AS "Hash_ID",
    created :: TIMESTAMPTZ,
    modified :: TIMESTAMPTZ,
    full_name,
    postcode,
    street,
    mobile_phone AS "phone",
    email,
    date_of_birth,
    ni_number,
    contact_for_research,
    contact_for_research_via,
    safe_to_contact,
    (SELECT COUNT(legalaid_thirdpartydetails.id) > 0 FROM legalaid_thirdpartydetails WHERE legalaid_thirdpartydetails.personal_details_id=pd.id) AS "Third Party Contact",
    (SELECT string_agg(laa_reference::varchar, ', ') FROM legalaid_case c WHERE c.personal_details_id=pd.id),
    (SELECT string_agg(c.laa_reference::varchar, ', ') FROM legalaid_thirdpartydetails t RIGHT JOIN legalaid_case c ON c.thirdparty_details_id=t.id WHERE t.personal_details_id=pd.id)
FROM
    legalaid_personaldetails AS pd
WHERE pd.contact_for_research = TRUE
    AND pd.safe_to_contact = 'SAFE'
    AND pd.created >= %s
    AND pd.created < %s
