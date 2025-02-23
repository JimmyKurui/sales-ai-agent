const CustomerInfoPanel = () => {
    return (
      <div className="w-80 bg-white border-l">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Customer Information</h3>
        </div>
  
        <div className="p-4 space-y-4">
          <CustomerProfile />
          <CustomerPersona />
          <SalesMetrics />
        </div>
      </div>
    );
  };
  
  const CustomerProfile = () => {
    return (
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-600">Profile</h4>
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
          <div>
            <p className="font-medium">John Doe</p>
            <p className="text-sm text-gray-500">john.doe@example.com</p>
          </div>
        </div>
      </div>
    );
  };
  
  const CustomerPersona = () => {
    return (
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-600">Persona</h4>
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-sm">Decision Maker</p>
          <p className="text-xs text-gray-500">Tech-savvy, Budget-conscious</p>
        </div>
      </div>
    );
  };
  
  const SalesMetrics = () => {
    return (
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-600">Metrics</h4>
        <div className="grid grid-cols-2 gap-2">
          <MetricCard title="Lifetime Value" value="$12,450" />
          <MetricCard title="Open Deals" value="2" />
        </div>
      </div>
    );
  };
  
  const MetricCard = ({ title, value }) => {
    return (
      <div className="bg-gray-50 p-3 rounded-lg">
        <p className="text-xs text-gray-500">{title}</p>
        <p className="font-medium">{value}</p>
      </div>
    );
  };
  
  export default CustomerInfoPanel;
  