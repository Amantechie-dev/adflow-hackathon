# AdFlow: AI-Powered Multi-Media Campaign Generator

AdFlow is an automated marketing generation engine built for modern businesses. By leveraging state-of-the-art Generative AI models alongside secure cloud infrastructure pipelines, AdFlow empowers teams to instantly create high-converting copy layouts and store campaign history flawlessly.

##  Key Features
* **AI Copywriting Core:** Uses advanced `gemini-2.5-flash` processing logic to craft professional headlines, body copy, and curated hashtags.
* **Hybrid Storage Architecture:** Programmatically uploads generated content copies directly to secure cloud object storage (Backblaze B2 distributed file network).
* **Local Transaction Logging:** Features an embedded transactional database architecture via `SQLite` to maintain full local processing history logs.
* **Sleek Web Interface:** Built using a high-performance web framework via `Streamlit` ensuring a smooth, responsive, user-friendly browser presentation.
* **Production-Grade Security:** Utilizes decoupled local variable loading systems via `.env` configuration matrices to eliminate credential leaks.

##  System Architecture
1. **User Interface:** Input product requirements via the Streamlit browser frontend.
2. **AI Layer:** Google Gemini dynamically processes copy requirements.
3. **Cloud Object Store:** Boto3 uploads text configurations securely via specific global regional endpoint matrices.
4. **Data Persistence:** Local SQLite indices update seamlessly to list historical tracking references in the sidebar log.

##  Installation & Local Setup

### 1. Clone the Workspace
```bash
git clone [https://github.com/Amantechie-dev/adflow-hackathon.git](https://github.com/Amantechie-dev/adflow-hackathon.git)
cd adflow-hackathon
