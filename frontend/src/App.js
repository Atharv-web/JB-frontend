import React, {useState, useRef, useEffect} from "react";
import './App.css';

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [botTypingText, setBotTypingText] = useState("")
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({behavior: "smooth"})
  }, [messages, botTypingText])


  const handleSend = async() => {
    if (!input.trim()) return
    const userMessage = {sender: "user", text : input}
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try{
      const res = await fetch("https://jb-frontend-w05y.onrender.com/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query:input}),
      })
      const data = await res.json()
      // await simulateTyping(data.answer)
      setMessages((prev) => [...prev, {sender:"bot", text: data.answer}])
      setBotTypingText("")
    } catch(err) {
      const errorMessage = {sender:"bot", text:"Error: Could not get response"}
      setMessages((prev) => [...prev, errorMessage])
    } finally{
      setLoading(false)
    }
  }

  const handleKeyPress = (e) =>{
    if (e.key === "Enter") handleSend()
  }


  return (
    <div className="app-container">
      <h1>JainBot</h1>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="message-bot">
            {botTypingText}
            <span className="typing-dots">
              {botTypingText && botTypingText.length % 3 === 0 ? "." : ""}
              {botTypingText && botTypingText.length % 3 === 1 ? ".." : ""}
              {botTypingText && botTypingText.length % 3 === 2 ? "..." : ""}   
            </span>
          </div>
        )}
        <div ref={chatEndRef}></div>
      </div>
      <div className="input-box">
        <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your Question.."
        />
        <button onClick={handleSend} disabled={loading}> Send</button>
      </div>
    </div>
  );
}

export default App;
