import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  Button
} from '@mui/material';
import CategoryIcon from '@mui/icons-material/Category';
import InfoIcon from '@mui/icons-material/Info';
import EcoIcon from '@mui/icons-material/Eco';
import FormatColorFillIcon from '@mui/icons-material/FormatColorFill';
import TextureIcon from '@mui/icons-material/Texture';
import WidgetsIcon from '@mui/icons-material/Widgets';

const MaterialLibrary = () => {
  const [tabValue, setTabValue] = useState(0);
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  // Material categories
  const categories = [
    { id: 'textiles', name: 'Textiles', icon: <TextureIcon /> },
    { id: 'plastics', name: 'Plastics', icon: <FormatColorFillIcon /> },
    { id: 'metals', name: 'Metals', icon: <WidgetsIcon /> },
    { id: 'wood', name: 'Wood', icon: <CategoryIcon /> },
    { id: 'ceramics', name: 'Ceramics', icon: <CategoryIcon /> },
    { id: 'composites', name: 'Composites', icon: <CategoryIcon /> },
  ];
  
  // Material properties
  const properties = [
    'Flexibility',
    'Durability',
    'Sustainability',
    'Cost',
    'Weight',
    'Thermal Resistance',
    'Chemical Resistance',
    'Recyclability'
  ];
  
  // Sample materials for each category
  const materials = {
    textiles: [
      { 
        name: 'Organic Cotton', 
        properties: { 
          flexibility: 'High', 
          durability: 'Medium', 
          sustainability: 'High',
          recyclability: 'High'
        },
        description: 'Organic cotton is grown without synthetic pesticides or fertilizers, making it more environmentally friendly than conventional cotton.',
        applications: ['Fashion', 'Home Goods', 'Packaging'],
        eco: true
      },
      { 
        name: 'Polyester', 
        properties: { 
          flexibility: 'Medium', 
          durability: 'High', 
          sustainability: 'Low',
          recyclability: 'Medium'
        },
        description: 'Polyester is a synthetic fabric known for its durability, wrinkle resistance, and quick-drying properties.',
        applications: ['Fashion', 'Home Goods', 'Automotive'],
        eco: false
      },
      { 
        name: 'Recycled Nylon', 
        properties: { 
          flexibility: 'Medium', 
          durability: 'High', 
          sustainability: 'Medium',
          recyclability: 'High'
        },
        description: 'Recycled nylon is made from post-consumer waste like fishing nets and carpet fibers, reducing landfill waste and ocean pollution.',
        applications: ['Fashion', 'Accessories', 'Sporting Goods'],
        eco: true
      }
    ],
    plastics: [
      { 
        name: 'ABS (Acrylonitrile Butadiene Styrene)', 
        properties: { 
          flexibility: 'Low', 
          durability: 'High', 
          sustainability: 'Low',
          recyclability: 'Medium'
        },
        description: 'ABS is a common thermoplastic polymer known for its impact resistance and toughness.',
        applications: ['Electronics', 'Automotive', 'Toys'],
        eco: false
      },
      { 
        name: 'PLA (Polylactic Acid)', 
        properties: { 
          flexibility: 'Low', 
          durability: 'Medium', 
          sustainability: 'High',
          recyclability: 'High'
        },
        description: 'PLA is a biodegradable thermoplastic derived from renewable resources such as corn starch or sugar cane.',
        applications: ['Packaging', 'Consumer Goods', '3D Printing'],
        eco: true
      },
      { 
        name: 'Recycled HDPE', 
        properties: { 
          flexibility: 'Low', 
          durability: 'High', 
          sustainability: 'Medium',
          recyclability: 'High'
        },
        description: 'Recycled High-Density Polyethylene is made from post-consumer plastic waste, primarily from bottles and containers.',
        applications: ['Packaging', 'Construction', 'Furniture'],
        eco: true
      }
    ],
    metals: [
      { 
        name: 'Aluminum', 
        properties: { 
          flexibility: 'Low', 
          durability: 'High', 
          sustainability: 'Medium',
          recyclability: 'High'
        },
        description: 'Aluminum is lightweight, corrosion-resistant, and highly recyclable, making it popular for various applications.',
        applications: ['Electronics', 'Packaging', 'Construction'],
        eco: true
      },
      { 
        name: 'Stainless Steel', 
        properties: { 
          flexibility: 'Low', 
          durability: 'Very High', 
          sustainability: 'Medium',
          recyclability: 'High'
        },
        description: 'Stainless steel is an alloy known for its resistance to corrosion, staining, and rust.',
        applications: ['Home Goods', 'Construction', 'Automotive'],
        eco: true
      },
      { 
        name: 'Titanium', 
        properties: { 
          flexibility: 'Low', 
          durability: 'Very High', 
          sustainability: 'Medium',
          recyclability: 'Medium'
        },
        description: 'Titanium is a strong, lightweight metal with excellent corrosion resistance and biocompatibility.',
        applications: ['Aerospace', 'Medical', 'Consumer Electronics'],
        eco: false
      }
    ],
    wood: [
      { 
        name: 'Bamboo', 
        properties: { 
          flexibility: 'Medium', 
          durability: 'High', 
          sustainability: 'Very High',
          recyclability: 'High'
        },
        description: 'Bamboo is a fast-growing grass that's stronger than many hardwoods and highly renewable.',
        applications: ['Furniture', 'Flooring', 'Home Goods'],
        eco: true
      },
      { 
        name: 'Reclaimed Wood', 
        properties: { 
          flexibility: 'Low', 
          durability: 'High', 
          sustainability: 'Very High',
          recyclability: 'High'
        },
        description: 'Reclaimed wood is salvaged from old structures, reducing the demand for newly harvested timber.',
        applications: ['Furniture', 'Flooring', 'Decorative Elements'],
        eco: true
      },
      { 
        name: 'FSC-Certified Oak', 
        properties: { 
          flexibility: 'Low', 
          durability: 'Very High', 
          sustainability: 'High',
          recyclability: 'Medium'
        },
        description: 'FSC-certified oak comes from responsibly managed forests that provide environmental, social, and economic benefits.',
        applications: ['Furniture', 'Flooring', 'Construction'],
        eco: true
      }
    ],
    ceramics: [
      { 
        name: 'Porcelain', 
        properties: { 
          flexibility: 'Very Low', 
          durability: 'High', 
          sustainability: 'Medium',
          recyclability: 'Low'
        },
        description: 'Porcelain is a ceramic material known for its strength, hardness, and translucence.',
        applications: ['Home Goods', 'Bathroom Fixtures', 'Decorative Elements'],
        eco: false
      },
      { 
        name: 'Recycled Glass Ceramic', 
        properties: { 
          flexibility: 'Very Low', 
          durability: 'High', 
          sustainability: 'High',
          recyclability: 'Medium'
        },
        description: 'Made from recycled glass, this ceramic material reduces waste while providing durability and aesthetic appeal.',
        applications: ['Countertops', 'Tiles', 'Decorative Elements'],
        eco: true
      }
    ],
    composites: [
      { 
        name: 'Carbon Fiber', 
        properties: { 
          flexibility: 'Low', 
          durability: 'Very High', 
          sustainability: 'Low',
          recyclability: 'Low'
        },
        description: 'Carbon fiber is a strong, lightweight material made from thin carbon filaments woven together.',
        applications: ['Aerospace', 'Automotive', 'Sporting Goods'],
        eco: false
      },
      { 
        name: 'Mycelium Composite', 
        properties: { 
          flexibility: 'Medium', 
          durability: 'Medium', 
          sustainability: 'Very High',
          recyclability: 'Very High'
        },
        description: 'Mycelium composites are made from the root structure of mushrooms, creating a sustainable alternative to synthetic materials.',
        applications: ['Packaging', 'Insulation', 'Furniture'],
        eco: true
      },
      { 
        name: 'Natural Fiber Composites', 
        properties: { 
          flexibility: 'Medium', 
          durability: 'High', 
          sustainability: 'High',
          recyclability: 'High'
        },
        description: 'These composites combine natural fibers like flax, hemp, or jute with biodegradable resins for eco-friendly performance.',
        applications: ['Automotive', 'Construction', 'Consumer Goods'],
        eco: true
      }
    ]
  };
  
  const currentCategory = categories[tabValue].id;
  const currentMaterials = materials[currentCategory] || [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Material Library
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Explore Materials by Category
        </Typography>
        <Typography variant="body1" paragraph>
          Browse our extensive library of materials optimized for different properties like flexibility, durability, and sustainability.
          Each material includes detailed specifications and recommended applications.
        </Typography>
        
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ mb: 3 }}
        >
          {categories.map((category) => (
            <Tab 
              key={category.id} 
              label={category.name} 
              icon={category.icon} 
              iconPosition="start"
            />
          ))}
        </Tabs>
        
        <Grid container spacing={3}>
          {currentMaterials.map((material, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card elevation={2} sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="h6" component="div">
                      {material.name}
                    </Typography>
                    {material.eco && (
                      <Chip 
                        icon={<EcoIcon />} 
                        label="Eco-Friendly" 
                        size="small" 
                        color="success"
                      />
                    )}
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {material.description}
                  </Typography>
                  
                  <Typography variant="subtitle2" gutterBottom>
                    Key Properties:
                  </Typography>
                  <Grid container spacing={1} sx={{ mb: 2 }}>
                    {Object.entries(material.properties).map(([key, value]) => (
                      <Grid item xs={6} key={key}>
                        <Chip 
                          label={`${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`}
                          size="small"
                          variant="outlined"
                          sx={{ width: '100%' }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                  
                  <Typography variant="subtitle2" gutterBottom>
                    Recommended Applications:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                    {material.applications.map((app, i) => (
                      <Chip key={i} label={app} size="small" />
                    ))}
                  </Box>
                  
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={() => {}}
                    sx={{ mt: 1 }}
                  >
                    Use in Design
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
      
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Material Properties Guide
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <List>
              {properties.slice(0, 4).map((property, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary={property} 
                      secondary={
                        property === 'Flexibility' ? 'How much the material can bend without breaking' :
                        property === 'Durability' ? 'Resistance to wear, pressure, or damage' :
                        property === 'Sustainability' ? 'Environmental impact and resource efficiency' :
                        'Relative price point compared to alternatives'
                      } 
                    />
                  </ListItem>
                  {index < 3 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))}
            </List>
          </Grid>
          <Grid item xs={12} md={6}>
            <List>
              {properties.slice(4).map((property, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary={property} 
                      secondary={
                        property === 'Weight' ? 'Mass relative to volume' :
                        property === 'Thermal Resistance' ? 'Ability to withstand heat without degrading' :
                        property === 'Chemical Resistance' ? 'Resistance to damage from chemicals' :
                        'Ability to be recycled at end of life'
                      } 
                    />
                  </ListItem>
                  {index < 3 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))}
            </List>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default MaterialLibrary;
