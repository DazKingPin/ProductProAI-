import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Button, 
  Tabs,
  Tab,
  TextField,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Divider,
  IconButton,
  Tooltip,
  Card,
  CardContent,
  CardMedia,
  Chip
} from '@mui/material';
import { styled } from '@mui/material/styles';
import SaveIcon from '@mui/icons-material/Save';
import UndoIcon from '@mui/icons-material/Undo';
import RedoIcon from '@mui/icons-material/Redo';
import ColorLensIcon from '@mui/icons-material/ColorLens';
import ViewInArIcon from '@mui/icons-material/ViewInAr';
import TextureIcon from '@mui/icons-material/Texture';
import TuneIcon from '@mui/icons-material/Tune';
import ShareIcon from '@mui/icons-material/Share';
import DownloadIcon from '@mui/icons-material/Download';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';

// Mock 3D model component
const Model = ({ color, material, size }) => {
  return (
    <mesh>
      <boxGeometry args={[size, size, size]} />
      <meshStandardMaterial color={color} roughness={material === 'Glossy' ? 0.1 : 0.8} />
    </mesh>
  );
};

// Custom styled components
const DesignPanel = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  height: '100%',
  display: 'flex',
  flexDirection: 'column'
}));

const CanvasContainer = styled(Box)(({ theme }) => ({
  flex: 1,
  backgroundColor: '#f0f0f0',
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
  position: 'relative'
}));

const ControlsContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: `1px solid ${theme.palette.divider}`
}));

const MaterialSwatch = styled(Box)(({ theme, selected }) => ({
  width: 60,
  height: 60,
  margin: theme.spacing(0.5),
  borderRadius: theme.shape.borderRadius,
  cursor: 'pointer',
  border: selected ? `2px solid ${theme.palette.primary.main}` : '2px solid transparent',
  '&:hover': {
    opacity: 0.9,
    transform: 'scale(1.05)'
  }
}));

const ColorSwatch = styled(Box)(({ theme, selected }) => ({
  width: 36,
  height: 36,
  borderRadius: '50%',
  cursor: 'pointer',
  border: selected ? `2px solid ${theme.palette.primary.main}` : '2px solid transparent',
  '&:hover': {
    opacity: 0.9,
    transform: 'scale(1.05)'
  }
}));

const DesignStudio = () => {
  const [tabValue, setTabValue] = useState(0);
  const [designName, setDesignName] = useState('New Design');
  const [selectedColor, setSelectedColor] = useState('#3f51b5');
  const [selectedMaterial, setSelectedMaterial] = useState('Matte');
  const [modelSize, setModelSize] = useState(1);
  const [industry, setIndustry] = useState('Furniture');
  const [commandInput, setCommandInput] = useState('');
  
  // Mock data
  const colors = ['#3f51b5', '#f44336', '#4caf50', '#ffc107', '#9c27b0', '#00bcd4', '#ff9800', '#795548'];
  const materials = ['Matte', 'Glossy', 'Textured', 'Metallic', 'Wood', 'Plastic'];
  const industries = ['Furniture', 'Electronics', 'Fashion', 'Packaging', 'Home Goods', 'Automotive'];
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleCommandSubmit = (e) => {
    e.preventDefault();
    // Mock NLP processing of command
    if (commandInput.toLowerCase().includes('color')) {
      if (commandInput.toLowerCase().includes('red')) {
        setSelectedColor('#f44336');
      } else if (commandInput.toLowerCase().includes('blue')) {
        setSelectedColor('#3f51b5');
      } else if (commandInput.toLowerCase().includes('green')) {
        setSelectedColor('#4caf50');
      }
    }
    
    if (commandInput.toLowerCase().includes('material')) {
      if (commandInput.toLowerCase().includes('glossy')) {
        setSelectedMaterial('Glossy');
      } else if (commandInput.toLowerCase().includes('wood')) {
        setSelectedMaterial('Wood');
      } else if (commandInput.toLowerCase().includes('metal')) {
        setSelectedMaterial('Metallic');
      }
    }
    
    if (commandInput.toLowerCase().includes('size')) {
      if (commandInput.toLowerCase().includes('larger') || commandInput.toLowerCase().includes('bigger')) {
        setModelSize(prev => Math.min(prev + 0.5, 2));
      } else if (commandInput.toLowerCase().includes('smaller')) {
        setModelSize(prev => Math.max(prev - 0.5, 0.5));
      }
    }
    
    setCommandInput('');
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Design Studio</Typography>
        <Box>
          <Button 
            variant="contained" 
            startIcon={<SaveIcon />}
            sx={{ mr: 1 }}
          >
            Save Design
          </Button>
          <Button 
            variant="outlined" 
            startIcon={<ShareIcon />}
          >
            Share
          </Button>
        </Box>
      </Box>
      
      <Grid container spacing={3}>
        {/* Left Panel - Design Controls */}
        <Grid item xs={12} md={3}>
          <DesignPanel elevation={3}>
            <Typography variant="h6" gutterBottom>Design Properties</Typography>
            
            <TextField
              label="Design Name"
              variant="outlined"
              fullWidth
              value={designName}
              onChange={(e) => setDesignName(e.target.value)}
              margin="normal"
              size="small"
            />
            
            <FormControl fullWidth margin="normal" size="small">
              <InputLabel>Industry</InputLabel>
              <Select
                value={industry}
                label="Industry"
                onChange={(e) => setIndustry(e.target.value)}
              >
                {industries.map((ind) => (
                  <MenuItem key={ind} value={ind}>{ind}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Divider sx={{ my: 2 }} />
            
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              variant="fullWidth"
              sx={{ mb: 2 }}
            >
              <Tab icon={<ColorLensIcon />} label="Color" />
              <Tab icon={<TextureIcon />} label="Material" />
              <Tab icon={<TuneIcon />} label="Properties" />
            </Tabs>
            
            {tabValue === 0 && (
              <Box>
                <Typography variant="subtitle2" gutterBottom>Color Selection</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', mb: 2 }}>
                  {colors.map((color) => (
                    <ColorSwatch 
                      key={color} 
                      bgcolor={color} 
                      selected={selectedColor === color}
                      onClick={() => setSelectedColor(color)}
                    />
                  ))}
                </Box>
                <TextField
                  label="Custom Color"
                  variant="outlined"
                  fullWidth
                  value={selectedColor}
                  onChange={(e) => setSelectedColor(e.target.value)}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </Box>
            )}
            
            {tabValue === 1 && (
              <Box>
                <Typography variant="subtitle2" gutterBottom>Material Selection</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
                  {materials.map((material) => (
                    <Tooltip title={material} key={material}>
                      <MaterialSwatch 
                        selected={selectedMaterial === material}
                        onClick={() => setSelectedMaterial(material)}
                        sx={{ 
                          backgroundColor: material === 'Metallic' ? '#a0a0a0' : 
                                          material === 'Wood' ? '#8B4513' : 
                                          material === 'Plastic' ? '#E0E0E0' : '#FFFFFF',
                          backgroundImage: material === 'Textured' ? 'linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%, #ccc), linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%, #ccc)' : 'none',
                          backgroundSize: material === 'Textured' ? '10px 10px' : 'auto',
                          backgroundPosition: material === 'Textured' ? '0 0, 5px 5px' : 'auto',
                          opacity: material === 'Glossy' ? 0.9 : 1,
                        }}
                      >
                        <Typography variant="caption" sx={{ 
                          position: 'absolute', 
                          bottom: 2, 
                          left: 0, 
                          right: 0, 
                          textAlign: 'center',
                          fontSize: '0.6rem',
                          color: material === 'Wood' || material === 'Metallic' ? 'white' : 'black'
                        }}>
                          {material}
                        </Typography>
                      </MaterialSwatch>
                    </Tooltip>
                  ))}
                </Box>
              </Box>
            )}
            
            {tabValue === 2 && (
              <Box>
                <Typography variant="subtitle2" gutterBottom>Size</Typography>
                <Slider
                  value={modelSize}
                  min={0.5}
                  max={2}
                  step={0.1}
                  onChange={(e, newValue) => setModelSize(newValue)}
                  valueLabelDisplay="auto"
                  marks={[
                    { value: 0.5, label: 'S' },
                    { value: 1, label: 'M' },
                    { value: 1.5, label: 'L' },
                    { value: 2, label: 'XL' },
                  ]}
                />
                
                <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>Other Properties</Typography>
                <FormControl fullWidth margin="normal" size="small">
                  <InputLabel>Finish</InputLabel>
                  <Select
                    value="Standard"
                    label="Finish"
                  >
                    <MenuItem value="Standard">Standard</MenuItem>
                    <MenuItem value="Premium">Premium</MenuItem>
                    <MenuItem value="Eco-friendly">Eco-friendly</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            )}
            
            <Box sx={{ mt: 'auto', pt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Natural Language Commands
              </Typography>
              <form onSubmit={handleCommandSubmit}>
                <TextField
                  fullWidth
                  placeholder="Type a command (e.g., 'Make it red')"
                  value={commandInput}
                  onChange={(e) => setCommandInput(e.target.value)}
                  size="small"
                  InputProps={{
                    endAdornment: (
                      <Button 
                        type="submit" 
                        variant="contained" 
                        size="small"
                        sx={{ ml: 1 }}
                      >
                        Apply
                      </Button>
                    )
                  }}
                />
              </form>
              <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                Try: "Change color to blue", "Make it glossy", "Increase size"
              </Typography>
            </Box>
          </DesignPanel>
        </Grid>
        
        {/* Center Panel - 3D Preview */}
        <Grid item xs={12} md={6}>
          <DesignPanel elevation={3}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">3D Preview</Typography>
              <Box>
                <Tooltip title="Undo">
                  <IconButton size="small" sx={{ mr: 1 }}>
                    <UndoIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Redo">
                  <IconButton size="small" sx={{ mr: 1 }}>
                    <RedoIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Download">
                  <IconButton size="small">
                    <DownloadIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>
            
            <CanvasContainer>
              <Canvas>
                <ambientLight intensity={0.5} />
                <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
                <PerspectiveCamera makeDefault position={[0, 0, 5]} />
                <Model color={selectedColor} material={selectedMaterial} size={modelSize} />
                <OrbitControls />
              </Canvas>
              
              <Box sx={{ 
                position: 'absolute', 
                bottom: 10, 
                left: 10, 
                backgroundColor: 'rgba(255,255,255,0.7)', 
                borderRadius: 1,
                px: 1,
                py: 0.5
              }}>
                <Typography variant="caption">
                  Use mouse to rotate | Scroll to zoom
                </Typography>
              </Box>
            </CanvasContainer>
            
            <ControlsContainer>
              <Grid container spacing={2} alignItems="center">
                <Grid item>
                  <Chip 
                    icon={<ColorLensIcon />} 
                    label={selectedColor} 
                    sx={{ backgroundColor: selectedColor, color: '#fff' }}
                  />
                </Grid>
                <Grid item>
                  <Chip icon={<TextureIcon />} label={selectedMaterial} />
                </Grid>
                <Grid item>
                  <Chip icon={<ViewInArIcon />} label={`Size: ${modelSize.toFixed(1)}`} />
                </Grid>
                <Grid item xs />
                <Grid item>
                  <Button 
                    variant="outlined" 
                    startIcon={<HelpOutlineIcon />}
                    size="small"
                  >
                    Help
                  </Button>
                </Grid>
              </Grid>
            </ControlsContainer>
          </DesignPanel>
        </Grid>
        
        {/* Right Panel - Suggestions & Standards */}
        <Grid item xs={12} md={3}>
          <DesignPanel elevation={3}>
            <Typography variant="h6" gutterBottom>Design Suggestions</Typography>
            
            <Typography variant="subtitle2" gutterBottom>
              Industry: {industry}
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="body2" paragraph>
                Based on your current design and industry standards, here are some suggestions:
              </Typography>
              
              <Card variant="outlined" sx={{ mb: 2 }}>
                <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
                  <Typography variant="subtitle2" color="primary">
                    Material Recommendation
                  </Typography>
                  <Typography variant="body2">
                    For {industry} products, consider using {industry === 'Furniture' ? 'sustainable wood' : industry === 'Electronics' ? 'recycled plastic' : 'eco-friendly materials'} to improve sustainability.
                  </Typography>
                </CardContent>
              </Card>
              
              <Card variant="outlined" sx={{ mb: 2 }}>
                <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
                  <Typography variant="subtitle2" color="primary">
                    Color Harmony
                  </Typography>
                  <Typography variant="body2">
                    Your current color works well with {
                      selectedColor === '#3f51b5' ? 'orange accents (#FF9800)' :
                      selectedColor === '#f44336' ? 'teal accents (#009688)' :
                      selectedColor === '#4caf50' ? 'purple accents (#9C27B0)' :
                      'complementary colors'
                    }.
                  </Typography>
                </CardContent>
              </Card>
              
              <Card variant="outlined">
                <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
                  <Typography variant="subtitle2" color="primary">
                    Industry Compliance
                  </Typography>
                  <Typography variant="body2">
                    Your design meets {industry} industry standards for dimensions and materials.
                  </Typography>
                </CardContent>
              </Card>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="h6" gutterBottom>Similar Designs</Typography>
            <Grid container spacing={1}>
              {[1, 2, 3, 4].map((item) => (
                <Grid item xs={6} key={item}>
                  <Card>
                    <CardMedia
                      component="div"
                      sx={{ 
                        height: 80, 
                        backgroundColor: '#e0e0e0',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      <Typography variant="caption" color="text.secondary">
                        [Design {item}]
                      </Typography>
                    </CardMedia>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </DesignPanel>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DesignStudio;
