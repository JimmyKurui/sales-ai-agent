import { MessageSquare, User, BarChart2, Target } from 'lucide-react';

const Sidebar = () => {
    return (
      <div className="w-16 bg-gray-900 flex flex-col items-center py-4">
        <div className="flex flex-col space-y-6">
          <SidebarIcon icon={<MessageSquare size={24} />} tooltip="Conversations" />
          <SidebarIcon icon={<User size={24} />} tooltip="Customers" />
          <SidebarIcon icon={<BarChart2 size={24} />} tooltip="Analytics" />
          <SidebarIcon icon={<Target size={24} />} tooltip="Goals" />
        </div>
      </div>
    );
  };

  const SidebarIcon = ({ icon, tooltip }) => {
    return (
      <div className="relative group">
        <div className="p-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg cursor-pointer">
          {icon}
        </div>
        <span className="absolute left-14 scale-0 transition-all rounded bg-gray-900 p-2 text-xs text-white group-hover:scale-100">
          {tooltip}
        </span>
      </div>
    );
  };
  
  export default Sidebar;