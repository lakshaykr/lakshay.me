
---

# RKN's Resume Website with Chat Feature 🚀

Welcome to RKN's Resume Website! This project showcases RKN's skills, experience, and education, along with an interactive chat feature where visitors can leave messages. The website is hosted on **GitHub Pages**, and the backend is powered by **Render**.

---

## Features ✨

- **Resume Content**:
  - About Me
  - Skills (Programming Languages, Soft Skills, Technical Skills)
  - Experience
  - Education
  - Friends Section (with profile pictures)

- **Interactive Chat**:
  - Visitors can leave messages with their username.
  - Messages are displayed in real-time.
  - Timestamps are shown in **Indian Standard Time (IST)**.

- **Dark/Light Mode**:
  - Toggle between dark and light themes.

- **Responsive Design**:
  - Works seamlessly on both desktop and mobile devices.

---

## Tech Stack 💻

- **Frontend**:
  - HTML, CSS, JavaScript
  - Hosted on **GitHub Pages**

- **Backend**:
  - Python (`http.server`)
  - PostgreSQL (for persistent chat storage)
  - Hosted on **Render**

---

## Setup Instructions 🛠️

### 1. Clone the Repository
```bash
git clone https://github.com/beingrkn/beingrkn.github.io.git
cd beingrkn.github.io
```

### 2. Set Up the Backend
1. **Create a PostgreSQL Database on Render**:
   - Go to your Render dashboard.
   - Click on **New** > **PostgreSQL**.
   - Configure the database and choose the free tier.
   - Copy the connection string.

2. **Update `server.py`**:
   - Replace the placeholder database connection string with the one from Render.
   - Ensure the `requirements.txt` file includes:
     ```
     psycopg2-binary
     pytz
     ```

3. **Deploy the Backend on Render**:
   - Push the code to GitHub.
   - Create a new **Web Service** on Render and connect it to your repository.
   - Set the environment variable `DATABASE_URL` with your PostgreSQL connection string.

### 3. Set Up the Frontend
1. **Update `script.js`**:
   - Replace the backend URL with your Render backend URL:
     ```javascript
      https://your-render-backend-url.onrender.com
     ```

2. **Host on GitHub Pages**:
   - Push the frontend code to GitHub.
   - Go to **Settings** > **Pages** and enable GitHub Pages for your repository.

---

## Common Issues and Solutions 🔧

### 1. **Chat Messages Take Time to Load Initially**
   - **Cause**: Render’s free tier puts services to sleep after 15 minutes of inactivity.
   - **Solution**:
     - Use a **cron job** to ping your backend every 10 minutes.
     - Example cron job:
       ```bash
       */10 * * * * curl -X GET https://your-render-backend-url.onrender.com/get-chats
       ```

### 2. **Chat Messages Disappear After Some Time**
   - **Cause**: Local file storage (`chats.json`) is ephemeral and gets reset when the service restarts.
   - **Solution**:
     - Use a **PostgreSQL database** to persist chat messages.

### 3. **Wrong Indian Standard Time (IST)**
   - **Cause**: Incorrect timezone handling in the backend.
   - **Solution**:
     - Use `pytz` or `zoneinfo` to handle timezones correctly.
     - Example:
       ```python
       from datetime import datetime
       import pytz

       ist = pytz.timezone('Asia/Kolkata')
       timestamp = datetime.now(ist).strftime('%d %b %Y, %I:%M %p IST')
       ```

### 4. **Cron Job Not Working**
   - **Cause**: The cron job might not be set up correctly or might not have the necessary permissions.
   - **Solution**:
     - Ensure the cron job script (`ping.sh`) is executable:
       ```bash
       chmod +x ping.sh
       ```
     - Verify the cron job is running by checking the logs:
       ```bash
       tail -f /var/log/syslog | grep CRON
       ```
     - If you’re using an online cron service, ensure the URL and schedule are configured correctly.

---

## Directory Structure 📂

```
project-folder/
│
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── server.py
├── requirements.txt
└── README.md
```

---

## Live Demo 🌐

- **Frontend**: [https://beingrkn.github.io](https://beingrkn.github.io)
- **Backend**: [https://beingrkn-github-io.onrender.com](https://beingrkn-github-io.onrender.com)

---

## Credits 🙌

- **RKN**: Developer and maintainer of the project.
- **Render**: For hosting the backend and database.
- **GitHub Pages**: For hosting the frontend.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy exploring the project! If you have any questions or issues, feel free to reach out. 😊

---
