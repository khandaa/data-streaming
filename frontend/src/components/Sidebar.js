import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import StreamIcon from '@mui/icons-material/Stream';
import TopicIcon from '@mui/icons-material/Topic';
import AppsIcon from '@mui/icons-material/Apps';
import HelpIcon from '@mui/icons-material/Help';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';

const drawerWidth = 250;

const menuItems = [
  { name: 'Dashboard', path: '/', icon: <DashboardIcon /> },
  { name: 'Stream Status', path: '/status', icon: <StreamIcon /> },
  { name: 'Kafka Topics', path: '/topics', icon: <TopicIcon /> },
  { name: 'Streaming Apps', path: '/apps', icon: <AppsIcon /> },
  { name: 'Help', path: '/help', icon: <HelpIcon /> },
];

const adminItems = [
  { name: 'Admin Dashboard', path: '/admin/dashboard', icon: <AdminPanelSettingsIcon /> },
];

function Sidebar({ open }) {
  const location = useLocation();
  const isLoggedIn = localStorage.getItem('user') !== null;

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Box sx={{ overflow: 'auto', mt: 8 }}>
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.name} disablePadding>
              <ListItemButton 
                component={Link} 
                to={item.path}
                selected={location.pathname === item.path}
              >
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.name} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        
        {isLoggedIn && (
          <>
            <Divider />
            <List>
              {adminItems.map((item) => (
                <ListItem key={item.name} disablePadding>
                  <ListItemButton 
                    component={Link} 
                    to={item.path}
                    selected={location.pathname === item.path}
                  >
                    <ListItemIcon>
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText primary={item.name} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </>
        )}
      </Box>
    </Drawer>
  );
}

export default Sidebar;
