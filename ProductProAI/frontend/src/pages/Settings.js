import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Switch,
  FormControlLabel,
  TextField,
  Button,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  Avatar,
  Card,
  CardContent,
  Alert,
  Tabs,
  Tab,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SecurityIcon from '@mui/icons-material/Security';
import LanguageIcon from '@mui/icons-material/Language';
import PaletteIcon from '@mui/icons-material/Palette';
import StorageIcon from '@mui/icons-material/Storage';
import CloudSyncIcon from '@mui/icons-material/CloudSync';
import ExtensionIcon from '@mui/icons-material/Extension';
import { useTheme } from '../context/ThemeContext';

const Settings = () => {
  const { theme, toggleTheme } = useTheme();
  const [tabValue, setTabValue] = useState(0);
  const [language, setLanguage] = useState('english');
  const [notifications, setNotifications] = useState({
    email: true,
    design: true,
    team: true,
    updates: false
  });
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };
  
  const handleNotificationChange = (name) => (event) => {
    setNotifications({
      ...notifications,
      [name]: event.target.checked
    });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        sx={{ mb: 3 }}
      >
        <Tab icon={<AccountCircleIcon />} label="Account" />
        <Tab icon={<PaletteIcon />} label="Appearance" />
        <Tab icon={<NotificationsIcon />} label="Notifications" />
        <Tab icon={<ExtensionIcon />} label="Integrations" />
      </Tabs>
      
      {tabValue === 0 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Account Settings
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card variant="outlined">
                <CardContent sx={{ textAlign: 'center' }}>
                  <Avatar 
                    sx={{ width: 100, height: 100, mx: 'auto', mb: 2 }}
                  >
                    U
                  </Avatar>
                  <Typography variant="h6">
                    User Name
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    user@example.com
                  </Typography>
                  <Button 
                    variant="outlined" 
                    sx={{ mt: 2 }}
                  >
                    Change Avatar
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={8}>
              <Box component="form" noValidate autoComplete="off">
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="First Name"
                      defaultValue="User"
                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Last Name"
                      defaultValue="Name"
                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email Address"
                      defaultValue="user@example.com"
                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Company/Organization"
                      defaultValue="Example Company"
                      variant="outlined"
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <FormControl fullWidth margin="normal">
                      <InputLabel>Industry</InputLabel>
                      <Select
                        value="furniture"
                        label="Industry"
                      >
                        <MenuItem value="furniture">Furniture</MenuItem>
                        <MenuItem value="electronics">Electronics</MenuItem>
                        <MenuItem value="packaging">Packaging</MenuItem>
                        <MenuItem value="fashion">Fashion</MenuItem>
                        <MenuItem value="homegoods">Home Goods</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
                
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button 
                    variant="contained" 
                    color="primary"
                  >
                    Save Changes
                  </Button>
                </Box>
              </Box>
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" gutterBottom>
                Security
              </Typography>
              <Button 
                variant="outlined" 
                color="primary"
                startIcon={<SecurityIcon />}
                sx={{ mr: 2 }}
              >
                Change Password
              </Button>
              <Button 
                variant="outlined" 
                color="secondary"
              >
                Two-Factor Authentication
              </Button>
            </Grid>
          </Grid>
        </Paper>
      )}
      
      {tabValue === 1 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Appearance Settings
          </Typography>
          
          <List>
            <ListItem>
              <ListItemIcon>
                <PaletteIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Theme" 
                secondary="Switch between light and dark mode"
              />
              <ListItemSecondaryAction>
                <FormControlLabel
                  control={
                    <Switch 
                      checked={theme === 'dark'} 
                      onChange={toggleTheme} 
                      color="primary"
                    />
                  }
                  label={theme === 'dark' ? "Dark" : "Light"}
                />
              </ListItemSecondaryAction>
            </ListItem>
            
            <Divider variant="inset" component="li" />
            
            <ListItem>
              <ListItemIcon>
                <LanguageIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Language" 
                secondary="Select your preferred language"
              />
              <ListItemSecondaryAction>
                <FormControl sx={{ minWidth: 120 }}>
                  <Select
                    value={language}
                    onChange={handleLanguageChange}
                    size="small"
                  >
                    <MenuItem value="english">English</MenuItem>
                    <MenuItem value="spanish">Spanish</MenuItem>
                    <MenuItem value="french">French</MenuItem>
                    <MenuItem value="german">German</MenuItem>
                    <MenuItem value="chinese">Chinese</MenuItem>
                  </Select>
                </FormControl>
              </ListItemSecondaryAction>
            </ListItem>
            
            <Divider variant="inset" component="li" />
            
            <ListItem>
              <ListItemIcon>
                <ExtensionIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Interface Density" 
                secondary="Adjust the spacing in the user interface"
              />
              <ListItemSecondaryAction>
                <FormControl sx={{ minWidth: 120 }}>
                  <Select
                    value="comfortable"
                    size="small"
                  >
                    <MenuItem value="compact">Compact</MenuItem>
                    <MenuItem value="comfortable">Comfortable</MenuItem>
                    <MenuItem value="spacious">Spacious</MenuItem>
                  </Select>
                </FormControl>
              </ListItemSecondaryAction>
            </ListItem>
          </List>
          
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button 
              variant="contained" 
              color="primary"
            >
              Save Preferences
            </Button>
          </Box>
        </Paper>
      )}
      
      {tabValue === 2 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Notification Settings
          </Typography>
          <Typography variant="body1" paragraph>
            Control how and when you receive notifications from ProductPro AI.
          </Typography>
          
          <List>
            <ListItem>
              <ListItemText 
                primary="Email Notifications" 
                secondary="Receive important updates via email"
              />
              <ListItemSecondaryAction>
                <Switch 
                  edge="end"
                  checked={notifications.email}
                  onChange={handleNotificationChange('email')}
                  color="primary"
                />
              </ListItemSecondaryAction>
            </ListItem>
            
            <Divider component="li" />
            
            <ListItem>
              <ListItemText 
                primary="Design Completion Alerts" 
                secondary="Get notified when AI completes a design task"
              />
              <ListItemSecondaryAction>
                <Switch 
                  edge="end"
                  checked={notifications.design}
                  onChange={handleNotificationChange('design')}
                  color="primary"
                />
              </ListItemSecondaryAction>
            </ListItem>
            
            <Divider component="li" />
            
            <ListItem>
              <ListItemText 
                primary="Team Collaboration" 
                secondary="Notifications about comments and shared projects"
              />
              <ListItemSecondaryAction>
                <Switch 
                  edge="end"
                  checked={notifications.team}
                  onChange={handleNotificationChange('team')}
                  color="primary"
                />
              </ListItemSecondaryAction>
            </ListItem>
            
            <Divider component="li" />
            
            <ListItem>
              <ListItemText 
                primary="Product Updates" 
                secondary="Learn about new features and improvements"
              />
              <ListItemSecondaryAction>
                <Switch 
                  edge="end"
                  checked={notifications.updates}
                  onChange={handleNotificationChange('updates')}
                  color="primary"
                />
              </ListItemSecondaryAction>
            </ListItem>
          </List>
          
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button 
              variant="outlined" 
              sx={{ mr: 2 }}
            >
              Reset to Default
            </Button>
            <Button 
              variant="contained" 
              color="primary"
            >
              Save Notification Settings
            </Button>
          </Box>
        </Paper>
      )}
      
      {tabValue === 3 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Integrations
          </Typography>
          <Typography variant="body1" paragraph>
            Connect ProductPro AI with other design software and services.
          </Typography>
          
          <Alert severity="info" sx={{ mb: 3 }}>
            Integrating with other design software allows you to seamlessly transfer designs between platforms and enhance your workflow.
          </Alert>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>A</Avatar>
                    <Typography variant="h6">
                      Adobe Creative Suite
                    </Typography>
                  </Box>
                  <Typography variant="body2" paragraph>
                    Connect with Adobe Creative Suite to import and export designs between ProductPro AI and Adobe applications.
                  </Typography>
                  <Button 
                    variant="contained" 
                    fullWidth
                  >
                    Connect
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>C</Avatar>
                    <Typography variant="h6">
                      CAD Software
                    </Typography>
                  </Box>
                  <Typography variant="body2" paragraph>
                    Integrate with popular CAD software to refine and finalize your 3D models for manufacturing.
                  </Typography>
                  <Button 
                    variant="contained" 
                    fullWidth
                  >
                    Connect
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>C</Avatar>
                    <Typography variant="h6">
                      Cloud Storage
                    </Typography>
                  </Box>
                  <Typography variant="body2" paragraph>
                    Connect with cloud storage services like Google Drive, Dropbox, or OneDrive to easily save and share your designs.
                  </Typography>
                  <Button 
                    variant="contained" 
                    fullWidth
                  >
                    Connect
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>P</Avatar>
                    <Typography variant="h6">
                      Project Management
                    </Typography>
                  </Box>
                  <Typography variant="body2" paragraph>
                    Integrate with project management tools like Asana, Trello, or Jira to track design tasks and deadlines.
                  </Typography>
                  <Button 
                    variant="contained" 
                    fullWidth
                  >
                    Connect
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
            <Button 
              variant="outlined" 
              startIcon={<ExtensionIcon />}
            >
              Browse More Integrations
            </Button>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default Settings;
