import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

// Create API context
export const ApiContext = createContext();

// API base URL
const API_BASE_URL = '/api';

// Create API provider component
export const ApiProvider = ({ children }) => {
  // State for API status
  const [apiStatus, setApiStatus] = useState({
    isLoading: true,
    isError: false,
    errorMessage: '',
    isConnected: false
  });

  // Check API connection on mount
  useEffect(() => {
    checkApiConnection();
  }, []);

  // Function to check API connection
  const checkApiConnection = async () => {
    try {
      setApiStatus(prev => ({ ...prev, isLoading: true }));
      const response = await axios.get(`${API_BASE_URL}/health`);
      
      if (response.data.status === 'healthy') {
        setApiStatus({
          isLoading: false,
          isError: false,
          errorMessage: '',
          isConnected: true
        });
      } else {
        setApiStatus({
          isLoading: false,
          isError: true,
          errorMessage: 'API is not healthy',
          isConnected: false
        });
      }
    } catch (error) {
      setApiStatus({
        isLoading: false,
        isError: true,
        errorMessage: error.message || 'Failed to connect to API',
        isConnected: false
      });
    }
  };

  // Process text command
  const processCommand = async (command, projectId = null) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/process-command`, {
        command,
        project_id: projectId
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process command');
    }
  };

  // Upload and analyze image
  const uploadImage = async (imageFile, projectId = null) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      
      if (projectId) {
        formData.append('project_id', projectId);
      }
      
      const response = await axios.post(`${API_BASE_URL}/upload-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to upload image');
    }
  };

  // Get all projects
  const getProjects = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/projects`);
      return response.data.projects;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get projects');
    }
  };

  // Create a new project
  const createProject = async (projectData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/projects`, projectData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to create project');
    }
  };

  // Get a specific project
  const getProject = async (projectId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/projects/${projectId}`);
      return response.data.project;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get project');
    }
  };

  // Update a project
  const updateProject = async (projectId, updateData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/projects/${projectId}`, updateData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to update project');
    }
  };

  // Delete a project
  const deleteProject = async (projectId) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/projects/${projectId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to delete project');
    }
  };

  // Analyze a project
  const analyzeProject = async (projectId) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/projects/${projectId}/analyze`);
      return response.data.analysis;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to analyze project');
    }
  };

  // Get recommendations for a project
  const getRecommendations = async (projectId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/projects/${projectId}/recommendations`);
      return response.data.recommendations;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get recommendations');
    }
  };

  // Get visualization data for a project
  const getVisualization = async (projectId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/projects/${projectId}/visualization`);
      return response.data.visualization;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get visualization');
    }
  };

  // Export project data
  const exportProject = async (projectId, format = 'json') => {
    try {
      const response = await axios.get(`${API_BASE_URL}/projects/${projectId}/export?format=${format}`);
      return response.data.export_data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to export project');
    }
  };

  // Get all materials
  const getMaterials = async (category = null) => {
    try {
      const url = category 
        ? `${API_BASE_URL}/materials?category=${category}` 
        : `${API_BASE_URL}/materials`;
      const response = await axios.get(url);
      return response.data.materials;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get materials');
    }
  };

  // Get a specific material
  const getMaterial = async (materialId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/materials/${materialId}`);
      return response.data.material;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get material');
    }
  };

  // Get all industry standards
  const getStandards = async (industry = null) => {
    try {
      const url = industry 
        ? `${API_BASE_URL}/standards?industry=${industry}` 
        : `${API_BASE_URL}/standards`;
      const response = await axios.get(url);
      return response.data.standards;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get standards');
    }
  };

  // Get a specific industry standard
  const getStandard = async (standardId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/standards/${standardId}`);
      return response.data.standard;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get standard');
    }
  };

  // Get design templates
  const getTemplates = async (industry = null) => {
    try {
      const url = industry 
        ? `${API_BASE_URL}/templates?industry=${industry}` 
        : `${API_BASE_URL}/templates`;
      const response = await axios.get(url);
      return response.data.templates;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get templates');
    }
  };

  // Get a specific design template
  const getTemplate = async (industry, templateId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/templates/${industry}/${templateId}`);
      return response.data.template;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get template');
    }
  };

  // Get industry configurations
  const getIndustryConfigs = async (industry = null) => {
    try {
      const url = industry 
        ? `${API_BASE_URL}/industry-configs?industry=${industry}` 
        : `${API_BASE_URL}/industry-configs`;
      const response = await axios.get(url);
      return response.data.configs;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get industry configs');
    }
  };

  // Get market trends
  const getTrends = async (industry = null) => {
    try {
      const url = industry 
        ? `${API_BASE_URL}/trends?industry=${industry}` 
        : `${API_BASE_URL}/trends`;
      const response = await axios.get(url);
      return response.data.trends;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get trends');
    }
  };

  // Get sustainable materials
  const getSustainableMaterials = async (category = null, minScore = null) => {
    try {
      let url = `${API_BASE_URL}/sustainability/materials`;
      const params = [];
      
      if (category) {
        params.push(`category=${category}`);
      }
      
      if (minScore) {
        params.push(`min_score=${minScore}`);
      }
      
      if (params.length > 0) {
        url += `?${params.join('&')}`;
      }
      
      const response = await axios.get(url);
      return response.data.materials;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get sustainable materials');
    }
  };

  // Create a collaboration session
  const createCollaborationSession = async (projectId, name = null) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/collaboration/sessions`, {
        project_id: projectId,
        name
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to create collaboration session');
    }
  };

  // Provide all API functions to components
  const apiContextValue = {
    apiStatus,
    checkApiConnection,
    processCommand,
    uploadImage,
    getProjects,
    createProject,
    getProject,
    updateProject,
    deleteProject,
    analyzeProject,
    getRecommendations,
    getVisualization,
    exportProject,
    getMaterials,
    getMaterial,
    getStandards,
    getStandard,
    getTemplates,
    getTemplate,
    getIndustryConfigs,
    getTrends,
    getSustainableMaterials,
    createCollaborationSession
  };

  return (
    <ApiContext.Provider value={apiContextValue}>
      {children}
    </ApiContext.Provider>
  );
};

// Custom hook to use the API context
export const useApi = () => {
  const context = React.useContext(ApiContext);
  if (context === undefined) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};
