*** Setting ***
Library     RequestsLibrary
Library     Collections

*** Test Cases ***

testget
    ${payload}=     Create Dictionary    eid=1
    Create Session    event    http://127.0.0.1:8000/api
    ${r}=     Get Request    event    /gget_event_list/    params=${payload}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}