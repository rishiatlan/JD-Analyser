import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemText,
  Chip,
  LinearProgress,
  Button,
} from '@mui/material';
import { JDAnalysisResponse } from '../services/api';

const AnalysisResults: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const analysis = location.state?.analysis as JDAnalysisResponse;

  if (!analysis) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          No analysis results found
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/')}
        >
          Go Back
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analysis Results
      </Typography>
      
      <Grid container spacing={3}>
        {/* Overall Score */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Overall Score
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box sx={{ flexGrow: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={analysis.overall_score * 100}
                  sx={{ height: 10, borderRadius: 5 }}
                />
              </Box>
              <Typography variant="h6">
                {Math.round(analysis.overall_score * 100)}%
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Sections */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Sections Analysis
            </Typography>
            {analysis.sections.map((section, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  {section.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {section.content}
                </Typography>
                {section.suggestions.length > 0 && (
                  <List dense>
                    {section.suggestions.map((suggestion, idx) => (
                      <ListItem key={idx}>
                        <ListItemText primary={suggestion} />
                      </ListItem>
                    ))}
                  </List>
                )}
              </Box>
            ))}
          </Paper>
        </Grid>

        {/* Bias Analysis */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Bias Analysis
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Inclusivity Score: {Math.round(analysis.bias_analysis.inclusivity_score * 100)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={analysis.bias_analysis.inclusivity_score * 100}
                sx={{ height: 10, borderRadius: 5, mb: 2 }}
              />
              {analysis.bias_analysis.biased_terms.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Biased Terms Found:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.bias_analysis.biased_terms.map((term, idx) => (
                      <Chip key={idx} label={term} color="error" />
                    ))}
                  </Box>
                </Box>
              )}
              <Typography variant="subtitle2" gutterBottom>
                Suggestions:
              </Typography>
              <List dense>
                {analysis.bias_analysis.suggestions.map((suggestion, idx) => (
                  <ListItem key={idx}>
                    <ListItemText primary={suggestion} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Paper>
        </Grid>

        {/* Readability Analysis */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Readability Analysis
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Readability Score: {Math.round(analysis.readability_analysis.score * 100)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={analysis.readability_analysis.score * 100}
                sx={{ height: 10, borderRadius: 5, mb: 2 }}
              />
              <Typography variant="subtitle2" gutterBottom>
                Complexity: {analysis.readability_analysis.complexity}
              </Typography>
              <List dense>
                {analysis.readability_analysis.suggestions.map((suggestion, idx) => (
                  <ListItem key={idx}>
                    <ListItemText primary={suggestion} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Paper>
        </Grid>

        {/* SEO Analysis */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              SEO Analysis
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Keywords Found:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {analysis.seo_analysis.keywords.map((keyword, idx) => (
                  <Chip key={idx} label={keyword} color="primary" />
                ))}
              </Box>
              {analysis.seo_analysis.missing_keywords.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Missing Keywords:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.seo_analysis.missing_keywords.map((keyword, idx) => (
                      <Chip key={idx} label={keyword} color="warning" />
                    ))}
                  </Box>
                </Box>
              )}
              <Typography variant="subtitle2" gutterBottom>
                Suggestions:
              </Typography>
              <List dense>
                {analysis.seo_analysis.suggestions.map((suggestion, idx) => (
                  <ListItem key={idx}>
                    <ListItemText primary={suggestion} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Paper>
        </Grid>

        {/* Action Buttons */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/')}
            >
              Back
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/enhanced', { state: { analysis } })}
            >
              View Enhanced Version
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalysisResults; 