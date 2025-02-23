import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { MessageSquare } from 'lucide-react';
import { wsService } from '../services/websocket';

const ClientChat = () => {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const { messages, isConnected } = useSelector((state) => state.chat);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const message = {
      type: 'client',
      content: input,
      timestamp: new Date().toISOString(),
    };
    

    wsService.sendMessage(message);
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm p-4">
        <div className="flex items-center space-x-2">
          <MessageSquare className="text-blue-500" />
          <h1 className="text-xl font-semibold">Sales Assistant</h1>
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ClientChatMessage key={index} {...message} />
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-4 bg-white border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
          />
          <button 
            type="submit"
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

const ClientChatMessage = ({ content, type, timestamp }) => {
  const isClient = type === 'client';
  
  return (
    <div className={`flex ${isClient ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[70%] rounded-lg p-3 ${
        isClient ? 'bg-blue-500 text-white' : 'bg-white shadow-sm'
      }`}>
        <p className="text-sm">{content}</p>
        <span className="text-xs opacity-70">
          {new Date(timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};

export default ClientChat