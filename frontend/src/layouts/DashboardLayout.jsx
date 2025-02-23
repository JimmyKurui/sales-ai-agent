import SidebarLayout from './SidebarLayout';
import ChatSection from '../components/chat/ChatSection';
import CustomerInfoPanel from '../components/panels/CustomerInfo';

const DashboardLayout = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <SidebarLayout />
      <div className="flex-1 flex">
        <ChatSection />
        <CustomerInfoPanel />
      </div>
    </div>
  );
};

export default DashboardLayout;