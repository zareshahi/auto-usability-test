robotframework
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome

*** Test Cases ***
Navigate To Page
    Open Browser To Page    http://localhost:3000
    Title Should Be    React Landing Page

Click On Features
    Click Element    //a[contains(text(),'Features')]
    Title Should Be    Features

Click On About
    Click Element    //a[contains(text(),'About')]
    Title Should Be    About

Click On Services
    Click Element    //a[contains(text(),'Services')]
    Title Should Be    Our Services

Click On Gallery
    Click Element    //a[contains(text(),'Gallery')]
    Title Should Be    Gallery

Click On Testimonials
    Click Element    //a[contains(text(),'Testimonials')]
    Title Should Be    What our clients say

Click On Team
    Click Element    //a[contains(text(),'Team')]
    Title Should Be    Meet the Team

Click On Contact
    Click Element    //a[contains(text(),'Contact')]
    Title Should Be    Get In Touch

Submit Contact Form
    Input Text    name=name    John Smith
    Input Text    name=email    john@example.com
    Input Text    name=message    This is a test message.
    Click Button    Send Message

*** Keywords ***
Open Browser To Page
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}