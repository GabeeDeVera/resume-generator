#import "cv.typ": *

#let cvdata = yaml("../compiler_artifacts/template.yml")

#let uservars = (
    headingfont: "Arial",
    bodyfont: "Arial",
    fontsize: 11pt, // 10pt, 11pt, 12pt
    linespacing: 6pt,
    sectionspacing: 0pt,
    showAddress:  true, // true/false show address in contact info
    showNumber: true,  // true/false show phone number in contact info
    showTitle: true,   // true/false show title in heading
    headingsmallcaps: false, // true/false use small caps for headings
    sendnote: false, // set to false to have sideways endnote
)

// setrules and showrules can be overridden by re-declaring it here
// #let setrules(doc) = {
//      // add custom document style rules here
//
//      doc
// }

#let customrules(doc) = {
    // add custom document style rules here
    set page(
        paper: "us-letter", // a4, us-letter
        numbering: "1 / 1",
        number-align: center, // left, center, right
        margin: 1.25cm, // 1.25cm, 1.87cm, 2.5cm
    )

    doc
}

#let cvinit(doc) = {
    doc = setrules(uservars, doc)
    doc = showrules(uservars, doc)
    doc = customrules(doc)

    doc
}

// each section body can be overridden by re-declaring it here
// #let cveducation = []

// ========================================================================== //

#show: doc => cvinit(doc)

#cvheading(cvdata, uservars)
#cveducation(cvdata)
#cvpublications(cvdata)
#cvawards(cvdata)
#cvacadprojects(cvdata)
#cvpersonalprojects(cvdata)
#cvwork(cvdata)
#cvaffiliations(cvdata)
#cvcertificates(cvdata)
#cvskills(cvdata)
#cvreferences(cvdata)
#endnote(uservars)
