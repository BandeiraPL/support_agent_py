// src/App.jsx
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Chat from "./pages/Chat";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route
          path="/"
          element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;

// src/pages/Login.jsx
import React, { useState } from "react";

function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    // Aqui conectaremos com o backend futuramente
    if (username && password) {
      setIsAuthenticated(true);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-600 to-indigo-800">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Entrar</h2>
        <input
          type="text"
          placeholder="Usuário"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 mb-4 border rounded-xl focus:outline-none focus:ring-2"
        />
        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-4 border rounded-xl focus:outline-none focus:ring-2"
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700"
        >
          Entrar
        </button>
      </div>
    </div>
  );
}

export default Login;

// src/pages/Chat.jsx
import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([
    { role: "system", content: "Olá! Em que posso ajudar?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setInput("");
    // Aqui entra o fetch para o backend com a resposta
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-white p-4 shadow-md text-xl font-bold">Assistente POP</header>
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl max-w-xl ${msg.role === "user" ? "ml-auto bg-blue-500 text-white" : "bg-gray-300"}`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <footer className="p-4 bg-white shadow-inner">
        <div className="flex">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Digite sua pergunta..."
            className="flex-1 p-2 border rounded-l-xl focus:outline-none"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-4 rounded-r-xl hover:bg-blue-700"
          >
            Enviar
          </button>
        </div>
      </footer>
    </div>
  );
}

export default Chat;
