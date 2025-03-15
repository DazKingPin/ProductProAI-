import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Button, TextField, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { useApi } from '../context/ApiContext';

const DesignSoftwareIntegration = () => {
  const { getProjects, exportProject } = useApi();
  
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [exportFormat, setExportFormat] = useState('json');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [exportResult, setExportResult] = useState(null);
  
  // Fetch projects on component mount
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const projectsData = await getProjects();
        setProjects(Object.values(projectsData));
        setLoading(false);
      } catch (err) {
        setError('Failed to load projects');
        setLoading(false);
      }
    };
    
    fetchProjects();
  }, [getProjects]);
  
  // Handle export to design software
  const handleExport = async () => {
    if (!selectedProject) {
      setError('Please select a project');
      return;
    }
    
    try {
      setLoading(true);
      const result = await exportProject(selectedProject, exportFormat);
      setExportResult(result);
      setLoading(false);
    } catch (err) {
      setError('Failed to export project');
      setLoading(false);
    }
  };
  
  // List of supported design software
  const designSoftware = [
    {
      name: 'AutoCAD',
      description: 'Export designs to AutoCAD for detailed engineering and technical drawings.',
      formats: ['dxf', 'dwg'],
      icon: '🏗️'
    },
    {
      name: 'Adobe Illustrator',
      description: 'Export designs to Adobe Illustrator for vector graphics editing and refinement.',
      formats: ['ai', 'svg'],
      icon: '🎨'
    },
    {
      name: 'Blender',
      description: 'Export 3D models to Blender for advanced 3D modeling and rendering.',
      formats: ['obj', 'fbx'],
      icon: '🧊'
    },
    {
      name: 'Fusion 360',
      description: 'Export designs to Fusion 360 for parametric modeling and CAD/CAM.',
      formats: ['f3d', 'step'],
      icon: '⚙️'
    },
    {
      name: 'Photoshop',
      description: 'Export design assets to Photoshop for image editing and compositing.',
      formats: ['psd', 'png'],
      icon: '📸'
    }
  ];
  
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Design Software Integration
      </Typography>
      
      <Typography variant="body1" paragraph>
        Seamlessly export your designs to popular design software for further refinement and professional finishing.
      </Typography>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Export Design
            </Typography>
            
            <Box component="form" sx={{ mt: 2 }}>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel id="project-select-label">Select Project</InputLabel>
                <Select
                  labelId="project-select-label"
                  value={selectedProject}
                  label="Select Project"
                  onChange={(e) => setSelectedProject(e.target.value)}
                >
                  <MenuItem value="">
                    <em>Select a project</em>
                  </MenuItem>
                  {projects.map((project) => (
                    <MenuItem key={project.id} value={project.id}>
                      {project.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel id="format-select-label">Export Format</InputLabel>
                <Select
                  labelId="format-select-label"
                  value={exportFormat}
                  label="Export Format"
                  onChange={(e) => setExportFormat(e.target.value)}
                >
                  <MenuItem value="json">JSON (Generic)</MenuItem>
                  <MenuItem value="dxf">DXF (AutoCAD)</MenuItem>
                  <MenuItem value="svg">SVG (Illustrator)</MenuItem>
                  <MenuItem value="obj">OBJ (3D Models)</MenuItem>
                  <MenuItem value="step">STEP (CAD)</MenuItem>
                </Select>
              </FormControl>
              
              <Button
                variant="contained"
                color="primary"
                onClick={handleExport}
                disabled={loading || !selectedProject}
                fullWidth
              >
                {loading ? 'Exporting...' : 'Export Design'}
              </Button>
            </Box>
            
            {exportResult && (
              <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Export Successful
                </Typography>
                <Typography variant="body2">
                  Format: {exportResult.metadata.format}
                </Typography>
                <Typography variant="body2">
                  Project: {exportResult.metadata.project_name}
                </Typography>
                <Typography variant="body2">
                  Date: {new Date(exportResult.metadata.export_date).toLocaleString()}
                </Typography>
                <Button 
                  variant="outlined" 
                  size="small" 
                  sx={{ mt: 1 }}
                  onClick={() => {
                    // In a real implementation, this would download the file
                    alert('Download started');
                  }}
                >
                  Download File
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Supported Design Software
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              {designSoftware.map((software) => (
                <Paper 
                  key={software.name} 
                  sx={{ 
                    p: 2, 
                    mb: 2, 
                    display: 'flex',
                    alignItems: 'flex-start'
                  }}
                  elevation={1}
                >
                  <Box sx={{ fontSize: '2rem', mr: 2 }}>
                    {software.icon}
                  </Box>
                  <Box>
                    <Typography variant="subtitle1">
                      {software.name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" paragraph>
                      {software.description}
                    </Typography>
                    <Typography variant="body2">
                      Supported formats: {software.formats.join(', ')}
                    </Typography>
                  </Box>
                </Paper>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Integration Features
        </Typography>
        
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="subtitle1" gutterBottom>
                Bidirectional Workflow
              </Typography>
              <Typography variant="body2">
                Changes made in external design software can be imported back into ProductPro AI, maintaining a seamless workflow between platforms.
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="subtitle1" gutterBottom>
                Preserve Design Intelligence
              </Typography>
              <Typography variant="body2">
                All design parameters, material properties, and compliance information are preserved when exporting to supported formats, ensuring no data is lost.
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="subtitle1" gutterBottom>
                Version Control
              </Typography>
              <Typography variant="body2">
                Track changes across different software platforms with our integrated version control system, allowing you to revert to previous designs if needed.
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default DesignSoftwareIntegration;
