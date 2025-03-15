import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Button, TextField, Divider } from '@mui/material';
import { useApi } from '../context/ApiContext';
import { useNavigate } from 'react-router-dom';

const Collaboration = () => {
  const { getProjects, createCollaborationSession } = useApi();
  const navigate = useNavigate();
  
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [sessionName, setSessionName] = useState('');
  const [collaborationSessions, setCollaborationSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
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
  
  // Create a new collaboration session
  const handleCreateSession = async () => {
    if (!selectedProject) {
      setError('Please select a project');
      return;
    }
    
    try {
      setLoading(true);
      const session = await createCollaborationSession(
        selectedProject.id,
        sessionName || `Collaboration on ${selectedProject.name}`
      );
      
      // Add the new session to the list
      setCollaborationSessions([...collaborationSessions, session]);
      
      // Reset form
      setSessionName('');
      setSelectedProject(null);
      
      setLoading(false);
    } catch (err) {
      setError('Failed to create collaboration session');
      setLoading(false);
    }
  };
  
  // Join an existing collaboration session
  const handleJoinSession = (sessionId) => {
    // In a real implementation, this would connect to the session
    // For now, we'll just navigate to the design studio with the session ID
    navigate(`/design-studio?session=${sessionId}`);
  };
  
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Team Collaboration
      </Typography>
      
      <Typography variant="body1" paragraph>
        Collaborate with team members on product designs in real-time. Create a new collaboration session or join an existing one.
      </Typography>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Create New Collaboration Session
            </Typography>
            
            <Box component="form" sx={{ mt: 2 }}>
              <TextField
                select
                fullWidth
                label="Select Project"
                value={selectedProject ? selectedProject.id : ''}
                onChange={(e) => {
                  const project = projects.find(p => p.id === e.target.value);
                  setSelectedProject(project);
                }}
                SelectProps={{
                  native: true,
                }}
                sx={{ mb: 2 }}
              >
                <option value="">Select a project</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </TextField>
              
              <TextField
                fullWidth
                label="Session Name (optional)"
                value={sessionName}
                onChange={(e) => setSessionName(e.target.value)}
                sx={{ mb: 2 }}
              />
              
              <Button
                variant="contained"
                color="primary"
                onClick={handleCreateSession}
                disabled={loading || !selectedProject}
                fullWidth
              >
                {loading ? 'Creating...' : 'Create Session'}
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Active Collaboration Sessions
            </Typography>
            
            {collaborationSessions.length === 0 ? (
              <Typography variant="body2" color="textSecondary">
                No active sessions. Create a new one to get started.
              </Typography>
            ) : (
              <Box>
                {collaborationSessions.map((session) => (
                  <Paper 
                    key={session.session_id} 
                    sx={{ 
                      p: 2, 
                      mb: 2, 
                      display: 'flex', 
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle1">
                        {session.name}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Project: {session.project_id}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Created: {new Date(session.created_at).toLocaleString()}
                      </Typography>
                    </Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={() => handleJoinSession(session.session_id)}
                    >
                      Join
                    </Button>
                  </Paper>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 4 }}>
        <Divider sx={{ mb: 3 }} />
        
        <Typography variant="h5" gutterBottom>
          Collaboration Features
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Real-time Design Editing
              </Typography>
              <Typography variant="body2">
                Multiple team members can work on the same design simultaneously. See changes in real-time and coordinate your efforts efficiently.
              </Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Commenting and Feedback
              </Typography>
              <Typography variant="body2">
                Leave comments on specific parts of the design. Provide feedback, suggest improvements, and track changes throughout the design process.
              </Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Design Software Integration
              </Typography>
              <Typography variant="body2">
                Seamlessly export designs to popular design software like AutoCAD and Adobe Creative Suite for further refinement and professional finishing.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default Collaboration;
