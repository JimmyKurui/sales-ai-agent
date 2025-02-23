import { useState } from 'react';
import ClientChat from '../../views/ClientChat';

const ChatSection = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  return (
    <div className="flex-1 flex flex-col">
      <div className="bg-white shadow-sm p-4 border-b">
        <h2 className="text-lg font-semibold">Active Conversation</h2>
      </div>

      <ClientChat type="agent" />
    </div>
  );
};

export default ChatSection;