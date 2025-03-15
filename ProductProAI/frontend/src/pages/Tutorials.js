import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia,
  CardActions,
  Button,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import SchoolIcon from '@mui/icons-material/School';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DesignServicesIcon from '@mui/icons-material/DesignServices';
import CategoryIcon from '@mui/icons-material/Category';
import GroupsIcon from '@mui/icons-material/Groups';
import EcoIcon from '@mui/icons-material/Eco';

const Tutorials = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [expanded, setExpanded] = useState('panel1');

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  // Tutorial categories
  const tutorialCategories = [
    {
      id: 'getting-started',
      title: 'Getting Started',
      description: 'Learn the basics of ProductPro AI and how to create your first design.',
      icon: <SchoolIcon />,
      tutorials: [
        {
          id: 'intro',
          title: 'Introduction to ProductPro AI',
          duration: '5 min',
          thumbnail: '/assets/tutorial1.jpg',
          description: 'Get an overview of ProductPro AI and its capabilities for product design.'
        },
        {
          id: 'first-design',
          title: 'Creating Your First Design',
          duration: '10 min',
          thumbnail: '/assets/tutorial2.jpg',
          description: 'Learn how to create a simple product design using the Design Studio.'
        },
        {
          id: 'image-upload',
          title: 'Using Reference Images',
          duration: '8 min',
          thumbnail: '/assets/tutorial3.jpg',
          description: 'Discover how to upload and use reference images for inspiration in your designs.'
        }
      ]
    },
    {
      id: 'advanced-features',
      title: 'Advanced Features',
      description: 'Explore advanced features and techniques for professional product design.',
      icon: <DesignServicesIcon />,
      tutorials: [
        {
          id: 'materials',
          title: 'Working with Materials',
          duration: '12 min',
          thumbnail: '/assets/tutorial4.jpg',
          description: 'Learn how to select and customize materials for different product types.'
        },
        {
          id: 'industry-standards',
          title: 'Compliance with Industry Standards',
          duration: '15 min',
          thumbnail: '/assets/tutorial5.jpg',
          description: 'Understand how to ensure your designs meet industry-specific standards and regulations.'
        },
        {
          id: 'sustainability',
          title: 'Designing for Sustainability',
          duration: '18 min',
          thumbnail: '/assets/tutorial6.jpg',
          description: 'Discover techniques for creating eco-friendly and sustainable product designs.'
        }
      ]
    },
    {
      id: 'collaboration',
      title: 'Collaboration Tools',
      description: 'Learn how to collaborate with team members on product design projects.',
      icon: <GroupsIcon />,
      tutorials: [
        {
          id: 'team-projects',
          title: 'Working with Team Projects',
          duration: '10 min',
          thumbnail: '/assets/tutorial7.jpg',
          description: 'Learn how to create and manage shared design projects with your team.'
        },
        {
          id: 'feedback',
          title: 'Giving and Receiving Feedback',
          duration: '8 min',
          thumbnail: '/assets/tutorial8.jpg',
          description: 'Discover effective ways to provide and incorporate design feedback.'
        }
      ]
    }
  ];

  // Getting started steps
  const gettingStartedSteps = [
    {
      label: 'Create an Account',
      description: `Start by creating your ProductPro AI account. This gives you access to all features and allows you to save your designs.`,
    },
    {
      label: 'Explore the Dashboard',
      description:
        'Familiarize yourself with the dashboard interface. Here you can see your recent projects, design capabilities, and material options.',
    },
    {
      label: 'Upload Reference Images',
      description: `Upload images that will serve as inspiration for your design. Our AI will analyze these images for shapes, colors, textures, and more.`,
    },
    {
      label: 'Create Your First Design',
      description: `Use the Design Studio to create your product. You can use natural language commands, adjust parameters manually, or combine both approaches.`,
    },
    {
      label: 'Save and Share',
      description: `Save your design and share it with team members or clients. You can export in various formats or continue refining your design.`,
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tutorials & Guides
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Getting Started with ProductPro AI
        </Typography>
        <Typography variant="body1" paragraph>
          Follow these simple steps to start creating professional product designs with ProductPro AI.
        </Typography>
        
        <Stepper activeStep={activeStep} orientation="vertical">
          {gettingStartedSteps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel>
                <Typography variant="subtitle1">{step.label}</Typography>
              </StepLabel>
              <StepContent>
                <Typography variant="body2">{step.description}</Typography>
                <Box sx={{ mb: 2, mt: 1 }}>
                  <div>
                    <Button
                      variant="contained"
                      onClick={handleNext}
                      sx={{ mt: 1, mr: 1 }}
                    >
                      {index === gettingStartedSteps.length - 1 ? 'Finish' : 'Continue'}
                    </Button>
                    <Button
                      disabled={index === 0}
                      onClick={handleBack}
                      sx={{ mt: 1, mr: 1 }}
                    >
                      Back
                    </Button>
                  </div>
                </Box>
              </StepContent>
            </Step>
          ))}
        </Stepper>
        {activeStep === gettingStartedSteps.length && (
          <Paper square elevation={0} sx={{ p: 3 }}>
            <Typography variant="body1" paragraph>
              All steps completed - you're ready to start designing!
            </Typography>
            <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
              Reset
            </Button>
            <Button 
              variant="contained" 
              onClick={() => window.location.href = '/upload'}
              startIcon={<CloudUploadIcon />}
              sx={{ mt: 1, mr: 1 }}
            >
              Upload Images
            </Button>
            <Button 
              variant="contained" 
              color="secondary"
              onClick={() => window.location.href = '/design-studio'}
              startIcon={<DesignServicesIcon />}
              sx={{ mt: 1, mr: 1 }}
            >
              Go to Design Studio
            </Button>
          </Paper>
        )}
      </Paper>
      
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Video Tutorials
      </Typography>
      
      {tutorialCategories.map((category) => (
        <Accordion 
          key={category.id}
          expanded={expanded === category.id}
          onChange={handleChange(category.id)}
          sx={{ mb: 2 }}
        >
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls={`${category.id}-content`}
            id={`${category.id}-header`}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {category.icon}
              <Typography variant="h6" sx={{ ml: 1 }}>
                {category.title}
              </Typography>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body1" paragraph>
              {category.description}
            </Typography>
            
            <Grid container spacing={3}>
              {category.tutorials.map((tutorial) => (
                <Grid item xs={12} sm={6} md={4} key={tutorial.id}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Box
                      sx={{
                        position: 'relative',
                        height: 160,
                        bgcolor: 'grey.200',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      <Typography variant="body2" color="text.secondary">
                        [Tutorial Thumbnail]
                      </Typography>
                      <Box
                        sx={{
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          bottom: 0,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}
                      >
                        <PlayCircleOutlineIcon sx={{ fontSize: 48, color: 'white' }} />
                      </Box>
                      <Chip 
                        label={tutorial.duration} 
                        size="small"
                        sx={{ 
                          position: 'absolute', 
                          bottom: 8, 
                          right: 8,
                          bgcolor: 'rgba(0,0,0,0.7)',
                          color: 'white'
                        }}
                      />
                    </Box>
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" gutterBottom>
                        {tutorial.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {tutorial.description}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<PlayCircleOutlineIcon />}>
                        Watch Tutorial
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </AccordionDetails>
        </Accordion>
      ))}
      
      <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Frequently Asked Questions
        </Typography>
        
        <List>
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="What types of products can I design with ProductPro AI?" 
              secondary="ProductPro AI supports a wide range of product categories including furniture, electronics, packaging, fashion, home goods, and more. The AI is trained on diverse design principles to meet the unique needs of each industry."
            />
          </ListItem>
          <Divider variant="inset" component="li" />
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="How does the image recognition feature work?" 
              secondary="When you upload reference images, our advanced AI analyzes them for elements such as shape, color, texture, and structural components. It then uses this analysis to generate design suggestions and 3D models based on your preferences."
            />
          </ListItem>
          <Divider variant="inset" component="li" />
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="Can I use natural language commands to modify my designs?" 
              secondary="Yes! ProductPro AI understands text commands like 'Make it blue' or 'Increase the size' to modify your designs. You can use these commands in the Design Studio to quickly make changes without manually adjusting parameters."
            />
          </ListItem>
          <Divider variant="inset" component="li" />
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="How does ProductPro AI ensure my designs meet industry standards?" 
              secondary="The system includes built-in compliance checks that automatically verify your designs against industry-specific standards and regulations. It will alert you to any potential issues and provide suggestions for bringing your design into compliance."
            />
          </ListItem>
          <Divider variant="inset" component="li" />
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="Can I collaborate with my team on designs?" 
              secondary="Absolutely! ProductPro AI includes robust collaboration tools that allow multiple team members to work on designs together, share feedback, and make collective decisions. You can also integrate with popular design software for further refinement."
            />
          </ListItem>
        </List>
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => window.location.href = '/upload'}
          >
            Start Designing Now
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Tutorials;
