import { useState } from 'react';

const ChatSection = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  return (
    <div className="flex-1 flex flex-col">
      <div className="bg-white shadow-sm p-4 border-b">
        <h2 className="text-lg font-semibold">Active Conversation</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage key={index} {...message} />
        ))}
      </div>

      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

const ChatMessage = ({ content, sender, timestamp }) => {
  const isAgent = sender === 'agent';

  return (
    <div className={`flex ${isAgent ? 'justify-start' : 'justify-end'}`}>
      <div className={`max-w-[70%] rounded-lg p-3 ${isAgent ? 'bg-white border' : 'bg-blue-500 text-white'}`}>
        <p className="text-sm">{content}</p>
        <span className="text-xs opacity-70">{timestamp}</span>
      </div>
    </div>
  );
};

export default ChatSection;