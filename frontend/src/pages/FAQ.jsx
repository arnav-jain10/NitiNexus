import { useState } from "react";
import { Link } from "react-router-dom";

const faqs = [
  ["How does NitiNexus recommend schemes?", "We compare the profile information you provide with the eligibility rules stored for each available scheme and show the strongest eligible matches first."],
  ["Why was I marked ineligible?", "The recommendations page explains the failed checks, such as category, income, purpose or requested loan amount."],
  ["What happens if my loan amount is below a scheme's minimum?", "That scheme is not recommended when a verified minimum loan value is present. The reason is also shown in the ineligible section."],
  ["Are the recommendations a guarantee of approval?", "No. NitiNexus is a discovery and matching tool. Final approval, documentation and sanction are decided by the authorized scheme or channel partner."],
  ["How are channel partners selected?", "Partners are filtered using the selected scheme and your saved state and district. If a district match is unavailable, the service can fall back to the state or multi-state directory where available."],
  ["Can I check the official scheme information?", "Yes. Each scheme includes an official-source link when one is available. Always confirm current terms, documents and application availability with the official source before applying."],
  ["Why might no channel partner be shown?", "Partner availability depends on the directory data, scheme support and location. The application also provides a map and navigation link when partner location information is available."],
  ["Is the EMI amount final?", "No. EMI is an estimate based on the selected rate, requested amount and tenure. Actual repayment terms can vary by the authorized lender or channel."],
];

export default function FAQ() {
  const [open, setOpen] = useState(0);
  return (
    <div className="page-frame faq-page">
      <div className="faq-card">
        <div className="faq-header">
          <div>
            <div className="eyebrow">HELP CENTER · FAQ</div>
            <h1>Frequently asked questions</h1>
            <p>Quick answers about scheme matching, eligibility, loan amounts, partners and EMI estimates.</p>
          </div>
          <Link className="inline-primary" to="/profile">Find a scheme →</Link>
        </div>
        <div className="faq-list">
          {faqs.map(([question, answer], index) => (
            <div className={`faq-item ${open === index ? "open" : ""}`} key={question}>
              <button type="button" onClick={() => setOpen(open === index ? -1 : index)} aria-expanded={open === index}>
                <span>{question}</span><strong>{open === index ? "−" : "+"}</strong>
              </button>
              {open === index && <p>{answer}</p>}
            </div>
          ))}
        </div>
        <div className="faq-note"><strong>Important:</strong> Scheme rules and partner availability can change. Use the official source and authorized partner for final confirmation.</div>
      </div>
    </div>
  );
}
