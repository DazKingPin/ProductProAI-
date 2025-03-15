import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  Alert,
  Button,
  Card,
  CardContent
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import VerifiedIcon from '@mui/icons-material/Verified';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import InfoIcon from '@mui/icons-material/Info';
import CategoryIcon from '@mui/icons-material/Category';

const IndustryStandards = () => {
  const [expanded, setExpanded] = useState(false);

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  // Industry standards data
  const industries = [
    {
      id: 'furniture',
      name: 'Furniture',
      icon: <CategoryIcon />,
      standards: [
        {
          name: 'BIFMA X5.1',
          description: 'Office Seating Standards',
          requirements: [
            'Weight capacity: 300 lbs minimum',
            'Stability testing for tipping resistance',
            'Durability testing for 100,000 cycles',
            'Arm strength testing for 250 lbs'
          ]
        },
        {
          name: 'California TB 117-2013',
          description: 'Flammability Standards for Upholstered Furniture',
          requirements: [
            'Flame retardant requirements for upholstery',
            'Smolder resistance testing',
            'Component testing methodology',
            'Labeling requirements'
          ]
        },
        {
          name: 'ASTM F1427',
          description: 'Safety of Bunk Beds',
          requirements: [
            'Guardrail height requirements',
            'Spacing between slats',
            'Entrapment testing',
            'Structural integrity testing'
          ]
        }
      ]
    },
    {
      id: 'electronics',
      name: 'Electronics',
      icon: <CategoryIcon />,
      standards: [
        {
          name: 'IEC 60950',
          description: 'Safety Standard for IT Equipment',
          requirements: [
            'Electric shock protection',
            'Energy hazards protection',
            'Fire hazard protection',
            'Mechanical hazards protection'
          ]
        },
        {
          name: 'RoHS Directive',
          description: 'Restriction of Hazardous Substances',
          requirements: [
            'Lead (Pb) < 0.1%',
            'Mercury (Hg) < 0.1%',
            'Cadmium (Cd) < 0.01%',
            'Hexavalent chromium (Cr6+) < 0.1%',
            'PBBs < 0.1%',
            'PBDEs < 0.1%'
          ]
        },
        {
          name: 'IP Rating System',
          description: 'Ingress Protection Rating',
          requirements: [
            'First digit (0-6): Protection against solid objects',
            'Second digit (0-9): Protection against liquids',
            'Common ratings: IP67 (dust-tight, immersion up to 1m)',
            'Testing methodology for verification'
          ]
        }
      ]
    },
    {
      id: 'packaging',
      name: 'Packaging',
      icon: <CategoryIcon />,
      standards: [
        {
          name: 'ISO 3394',
          description: 'Packaging Dimensions',
          requirements: [
            'Standard module dimensions: 600mm x 400mm',
            'Sub-modules: 400mm x 300mm, 300mm x 200mm',
            'Height variations allowed',
            'Stackability requirements'
          ]
        },
        {
          name: 'ASTM D4169',
          description: 'Performance Testing of Shipping Containers',
          requirements: [
            'Vibration testing',
            'Drop testing',
            'Compression testing',
            'Environmental conditioning'
          ]
        },
        {
          name: 'EU Directive 94/62/EC',
          description: 'Packaging and Packaging Waste',
          requirements: [
            'Minimization of packaging weight and volume',
            'Design for reuse and recovery',
            'Minimization of hazardous substances',
            'Heavy metals content limitations'
          ]
        }
      ]
    },
    {
      id: 'fashion',
      name: 'Fashion',
      icon: <CategoryIcon />,
      standards: [
        {
          name: 'ASTM D5489',
          description: 'Care Labeling of Textile Apparel',
          requirements: [
            'Washing instructions',
            'Drying instructions',
            'Ironing instructions',
            'Dry cleaning instructions'
          ]
        },
        {
          name: 'CPSC 16 CFR Part 1610',
          description: 'Flammability of Clothing Textiles',
          requirements: [
            'Class 1: Normal flammability',
            'Class 2: Intermediate flammability',
            'Class 3: Rapid and intense burning (prohibited)',
            'Testing methodology'
          ]
        },
        {
          name: 'OEKO-TEX Standard 100',
          description: 'Testing for Harmful Substances',
          requirements: [
            'pH value testing',
            'Formaldehyde limits',
            'Heavy metals testing',
            'Pesticide residue testing'
          ]
        }
      ]
    },
    {
      id: 'homegoods',
      name: 'Home Goods',
      icon: <CategoryIcon />,
      standards: [
        {
          name: 'ASTM F963',
          description: 'Toy Safety Standard',
          requirements: [
            'Small parts testing',
            'Sharp points and edges testing',
            'Flammability testing',
            'Heavy metals content limitations'
          ]
        },
        {
          name: 'NSF/ANSI 51',
          description: 'Food Equipment Materials',
          requirements: [
            'Material safety for food contact',
            'Cleanability requirements',
            'Corrosion resistance',
            'Non-toxicity verification'
          ]
        },
        {
          name: 'CPSC 16 CFR Part 1633',
          description: 'Flammability of Mattress Sets',
          requirements: [
            'Open flame testing',
            'Heat release rate limitations',
            'Testing methodology',
            'Labeling requirements'
          ]
        }
      ]
    }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Industry Standards
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Compliance Checker
        </Typography>
        <Typography variant="body1" paragraph>
          Ensure your product designs meet industry-specific standards and regulations. 
          Our AI automatically checks designs against these requirements to ensure compliance.
        </Typography>
        
        <Alert severity="info" sx={{ mb: 3 }}>
          Select an industry below to view applicable standards. When you create designs in the Design Studio, 
          ProductPro AI will automatically check compliance with these standards.
        </Alert>
        
        {industries.map((industry) => (
          <Accordion 
            key={industry.id}
            expanded={expanded === industry.id}
            onChange={handleChange(industry.id)}
            sx={{ mb: 2 }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`${industry.id}-content`}
              id={`${industry.id}-header`}
            >
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                {industry.icon}
                <Typography variant="h6" sx={{ ml: 1 }}>
                  {industry.name} Standards
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={3}>
                {industry.standards.map((standard, index) => (
                  <Grid item xs={12} md={4} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <VerifiedIcon color="primary" sx={{ mr: 1 }} />
                          <Typography variant="h6">
                            {standard.name}
                          </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          {standard.description}
                        </Typography>
                        <Typography variant="subtitle2" gutterBottom>
                          Key Requirements:
                        </Typography>
                        <List dense>
                          {standard.requirements.map((req, i) => (
                            <ListItem key={i} sx={{ py: 0 }}>
                              <ListItemIcon sx={{ minWidth: 30 }}>
                                <CheckCircleIcon fontSize="small" color="success" />
                              </ListItemIcon>
                              <ListItemText primary={req} />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </AccordionDetails>
          </Accordion>
        ))}
      </Paper>
      
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Compliance Verification Process
        </Typography>
        <Typography variant="body1" paragraph>
          ProductPro AI uses a comprehensive verification process to ensure your designs meet all applicable standards.
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" color="primary" gutterBottom>
                  Automatic Compliance Checks
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Dimensional Analysis" 
                      secondary="Verifies that your design meets size and proportion requirements for the selected industry" 
                    />
                  </ListItem>
                  <Divider variant="inset" component="li" />
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Material Compatibility" 
                      secondary="Checks if selected materials comply with industry regulations for safety and performance" 
                    />
                  </ListItem>
                  <Divider variant="inset" component="li" />
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Safety Feature Verification" 
                      secondary="Identifies required safety features and confirms their presence in your design" 
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
            
            <Button 
              variant="contained" 
              color="primary" 
              fullWidth
              onClick={() => window.location.href = '/design-studio'}
            >
              Check Your Design
            </Button>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" color="primary" gutterBottom>
                  Compliance Report
                </Typography>
                <Typography variant="body2" paragraph>
                  After analysis, ProductPro AI generates a detailed compliance report that includes:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  <Chip icon={<CheckCircleIcon />} label="Compliance Status" color="success" />
                  <Chip icon={<WarningIcon />} label="Potential Issues" color="warning" />
                  <Chip icon={<InfoIcon />} label="Recommendations" />
                </Box>
                <Alert severity="success" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    <strong>Sample Result:</strong> Your furniture design meets BIFMA X5.1 standards for office seating.
                  </Typography>
                </Alert>
                <Alert severity="warning">
                  <Typography variant="body2">
                    <strong>Sample Warning:</strong> Consider increasing the thickness of support beams to fully comply with load-bearing requirements.
                  </Typography>
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default IndustryStandards;
