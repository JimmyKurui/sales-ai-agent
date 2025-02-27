import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { wsService } from '../services/socketio';
import { addMessage } from '../stores/slices/chatSlice';
import { MessageSquare } from 'lucide-react';


const ClientChat = ({ type='client' }) => {
  const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const { messages, isConnected } = useSelector((state) => state.chat);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const message = {
      type,
      content: input,
      timestamp: new Date().toISOString(),
    };
    
    wsService.sendMessage(message);
    dispatch(addMessage(message));
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm p-4">
        <div className="flex items-center space-x-2">
          <MessageSquare className="text-blue-500" />
          <h1 className="text-xl font-semibold">CRM Runners | Sales</h1>
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>
      </header>

      {/* <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ClientChatMessage key={index} {...message, isAuthenticated} />
        ))}
      </div> */}

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {
          messages.map((message, index) => {
            return (
              <ClientChatMessage key={message.id} {...{...message, x: isAuthenticated}} />
            );
          })
        }
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

const ClientChatMessage = ({ content, type, timestamp, isAuthenticated }) => {
  const rightAligned = (type === 'client' && isAuthenticated) || (type === 'agent' && !isAuthenticated);
  
  return (
    <div className={`flex ${rightAligned ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[70%] rounded-lg p-3 ${
        rightAligned ? 'bg-blue-500 text-white' : 'bg-white shadow-sm'
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