// EJEMPLO FICTICIO. Ninguna persona, empresa ni cifra de este fichero es real.
// Sirve de plantilla: la skill (cv-a-medida en español, cv-tailoring en inglés) escribe un
// cv-content.js con este formato en la carpeta de cada candidatura, a partir de tu banco
// de evidencias. Para probarlo:
//   CV_CONTENT=tools/cv-content.example.js node tools/build-cv.js prueba.docx
//
// Formato: module.exports = (h) => [ ...párrafos... ], donde `h` son los helpers
// de build-cv.js. Las empresas de aquí deben coincidir con la sección 2 del banco
// (CARRERA-EVIDENCIAS.example.md o CAREER-EVIDENCE.example.md, que tienen las mismas)
// para que validate-cv.py no las marque como inventadas.
module.exports = (h) => [
  h.name('Jane Doe'),
  h.headline('Senior Engineering Manager | AI Delivery Teams, Team Growth & AI-Assisted Engineering'),
  h.contact('London, United Kingdom  |  +44 20 7946 0100  |  jane.doe@example.com'),
  h.contact('linkedin.com/in/jane-doe-example  |  github.com/jane-doe-example'),

  h.section('PROFESSIONAL SUMMARY'),
  h.para([['Senior engineering manager with 15+ years leading and growing engineering teams across SaaS, healthtech and e-commerce, including a CTO role, now focused on shipping applied AI into production and on how engineering teams work with AI. Delivered an AI auto-moderation system processing over 400,000 reviews per month that cut moderation costs by 1M GBP per year, and designed and runs a 13-agent autonomous publishing platform, 3+ months in continuous production. Leads through coaching: turns underperforming groups into high-performing teams, raising engagement to top-of-company levels (eNPS 40) while doubling delivery output and cutting cycle time by up to 50%.', false]]),

  h.section('CORE SKILLS'),
  h.skillLine('Engineering Leadership', 'Team Management, Hiring and Team Growth, Mentoring and Career Development, One-on-Ones and Performance Management, Turnaround to High Performance, Engagement and Team Health'),
  h.skillLine('Applied AI Engineering', 'LLM Agent Systems, Multi-Agent Orchestration, Agent Design and Evaluation, Output Guardrails, Inference Cost Control, Kubernetes-Based Services'),
  h.skillLine('AI-Assisted Engineering', 'Spec-Driven Development, AI Coding Assistants Across the SDLC, Repeatable AI-Assisted Operating Model, Code Quality and Review Automation'),
  h.skillLine('Delivery and Platform', 'End-to-End Delivery, Planning and Prioritization, Delivery Metrics (DORA, SPACE), Cycle Time and Throughput, Containerized Microservices, Reliability and Incident Response'),

  h.section('PROFESSIONAL EXPERIENCE'),

  h.jobTitle('Senior Engineering Manager'),
  h.jobMeta('Lumina Labs  |  London, United Kingdom  |  September 2025 - Present'),
  h.bullet([['Doubled engineering delivery output', true], [' by redefining ownership boundaries, sharpening prioritization and introducing predictable execution rituals.', false]]),
  h.bullet([['Raised team engagement by 40%', true], [' by closing historic leadership gaps and building a culture of direct, continuous and psychologically safe feedback anchored in regular one-on-ones.', false]]),
  h.bullet([['Introduced Spec-Driven Development, aligning product, design and engineering on scope and acceptance criteria before any code and ', false], ['reducing cycle time from 4d 2h to 2d 6h, approximately 45%', true], ['.', false]]),
  h.bullet([['Embedded AI coding assistants across the full development lifecycle', true], [', from requirements analysis to code review, QA and documentation, turning AI-assisted delivery into a repeatable team operating model.', false]]),

  h.jobTitle('Senior Engineering Manager'),
  h.jobMeta('Meridian Health  |  London, United Kingdom  |  September 2023 - September 2025'),
  h.bullet([['Turned an underperforming group into a high-performing team through restructuring, culture reset and foundational engineering metrics, achieving a ', false], ['sustained 50% reduction in cycle time', true], ['.', false]]),
  h.bullet([['Boosted team engagement to the second-highest level in the company after reorganization, ', false], ['reaching eNPS 40', true], ['.', false]]),
  h.bullet([['Delivered an AI-based auto-moderation system processing over 400,000 reviews per month for a global marketplace, ', false], ['reducing moderation costs by 1M GBP per year', true], ['.', false]]),
  h.bullet([['Reduced the LLM inference bill', true], [' through model selection and a push toward more deterministic outputs.', false]]),

  h.jobTitle('Chief Technology Officer'),
  h.jobMeta('Corveo  |  London, United Kingdom  |  November 2021 - June 2023  |  Regulated healthtech (telemedicine)'),
  h.bullet([['Scaled the engineering organization ', false], ['from 8 to 16 engineers', true], [' across backend, frontend, mobile and QA, hiring across disciplines while sustaining delivery throughout the growth.', false]]),
  h.bullet([['Established the operating model for code review, deployment and incident response, ', false], ['reducing production defects by 35% and MTTR by 40%', true], ['.', false]]),
  h.bullet([['Architected the migration from monolith to microservices-based APIs on Kubernetes, ', false], ['raising availability from 99.2% to 99.95%', true], [' and supporting 5x user growth.', false]]),

  h.jobTitle('Founder'),
  h.jobMeta('Harbor Goods  |  Bristol, United Kingdom  |  October 2009 - August 2026  |  Parallel entrepreneurial venture'),
  h.bullet([['Shipped a conversational AI chatbot into production on the e-commerce storefront, ', false], ['lifting conversion by 20%', true], ['.', false]]),
  h.bullet([['Divested the business in 2026', true], [' after building it into a self-sustaining, AI-automated operation, completing a 17-year founder journey.', false]]),

  h.jobTitle('R&D Manager'),
  h.jobMeta('FreightLink  |  London, United Kingdom  |  February 2020 - October 2021'),
  h.bullet([['Mentored senior engineers into leadership roles', true], [', strengthening internal succession and team autonomy.', false]]),
  h.bullet([['Owned the roadmap for migrating from monolithic systems to microservices, reducing technical debt and increasing delivery speed.', false]]),

  h.jobTitle('Head of Development'),
  h.jobMeta('Dermex  |  London, United Kingdom  |  February 2019 - February 2020  |  Pharmaceutical and dermocosmetics'),
  h.bullet([['Created a high-performing engineering team and introduced Agile practices across legacy and new systems.', false]]),
  h.bullet([['Implemented automated testing and continuous integration routines that ', false], ['decreased release defects by approximately 25%', true], [' and shortened release cycles.', false]]),

  h.jobTitle('Head of Development'),
  h.jobMeta('RideNow  |  London, United Kingdom  |  September 2016 - January 2019'),
  h.bullet([['Led the development organization and ', false], ['improved team productivity by approximately 40%', true], [' through clearer ownership and better review practices.', false]]),

  h.section('EDUCATION AND LANGUAGES'),
  h.eduLine('Executive MBA', 'Thames Business School, London'),
  h.eduLine('BSc Computer Science', 'University of Bristol'),
  h.eduLine('Postgraduate Degree in e-Commerce and Digital Marketing', 'Thames Business School, London'),
  h.skillLine('Languages', 'English (native), Spanish (full professional), French (native)'),

  h.signature('No fancy design here, and that\'s on purpose: this CV is ATS-optimized so a machine reads it as well as you do.'),
];
