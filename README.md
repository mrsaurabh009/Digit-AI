
# Digit AI ✍️🔢

A powerful and responsive **Handwritten Digit Recognition** web application powered by **Convolutional Neural Networks (CNN)**, built using **Flask, TensorFlow, HTML5, CSS3**, and **JavaScript**.

> 🎯 Predict digits drawn by the user live in the browser  
> 💡 Built for ML portfolio projects, education, and real-world use cases  
> 🚀 Deployed on Render: [Visit Live App](https://your-app-url.onrender.com)

---

## 🌟 Features

- 🎨 **Live Drawing Canvas** – Draw digits directly in-browser
- 🤖 **Deep Learning Model** – Trained on the MNIST dataset with over 93% accuracy
- ⚡ **Real-time Predictions** – Using a deployed CNN model with Flask backend
- 📱 **Fully Responsive UI** – HTML5 + CSS3 + JS + mobile-friendly design
- ☁️ **Hosted on Render** – Free tier deployment with backend + frontend

---

## 📸 Preview

![Digit AI Demo](https://your-screenshot-or-gif-url.com)

---

## 🧠 Tech Stack

| Layer         | Tools Used                           |
|---------------|---------------------------------------|
| Frontend      | HTML5, CSS3, JavaScript               |
| Backend       | Flask (Python)                        |
| Model         | CNN using TensorFlow & Keras          |
| Deployment    | Render (Python Web Service)           |
| Data          | MNIST Handwritten Digits Dataset      |

---

## 🛠️ Installation (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/digit-ai.git
   cd digit-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 🚀 Deploy on Render (or Replit, Railway)

> You can deploy this app to Render in less than 5 minutes!

1. Add `requirements.txt` and `render.yaml`
2. Push code to GitHub
3. Create new Web Service on [Render](https://render.com)
4. Set:
   - Runtime: Python 3
   - Build Command: *(leave blank)*
   - Start Command: `gunicorn app:app`

---

## 📁 Project Structure

```
digit-ai/
├── app.py
├── digit_model.h5
├── requirements.txt
├── render.yaml
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   └── about.html
```

---

## 📚 Dataset

- [MNIST Digits Dataset](http://yann.lecun.com/exdb/mnist/)
- 60,000 training images + 10,000 test images
- Each image is 28x28 grayscale handwritten digits (0–9)

---

## 🙋‍♂️ Contributors

- 👨‍💻 Saurabh Kumar – [LinkedIn](https://www.linkedin.com/in/saurabhkumardigit/) | [GitHub](https://github.com/saurabh123-digit)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Feedback

Feel free to open issues, submit PRs, or connect with me on [LinkedIn](https://www.linkedin.com/in/saurabhkumardigit/) for suggestions and improvements!
