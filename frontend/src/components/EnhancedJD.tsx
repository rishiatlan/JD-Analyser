import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Divider,
  Grid,
} from '@mui/material';
import { JDAnalysisResponse, enhanceJD } from '../services/api';

const EnhancedJD: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const analysis = location.state?.analysis as JDAnalysisResponse;
  const [enhancedContent, setEnhancedContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchEnhancedJD = async () => {
      if (!analysis) return;

      setLoading(true);
      setError('');

      try {
        const response = await enhanceJD(analysis.sections.map(s => s.content).join('\n\n'));
        setEnhancedContent(response.content);
      } catch (err) {
        setError('Error enhancing job description. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchEnhancedJD();
  }, [analysis]);

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
        Enhanced Job Description
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Typography color="error">{error}</Typography>
            ) : (
              <>
                <Typography variant="h6" gutterBottom>
                  Original Version
                </Typography>
                <Typography
                  variant="body1"
                  sx={{ whiteSpace: 'pre-wrap', mb: 3 }}
                >
                  {analysis.sections.map(s => s.content).join('\n\n')}
                </Typography>

                <Divider sx={{ my: 3 }} />

                <Typography variant="h6" gutterBottom>
                  Enhanced Version
                </Typography>
                <Typography
                  variant="body1"
                  sx={{ whiteSpace: 'pre-wrap' }}
                >
                  {enhancedContent}
                </Typography>
              </>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/analysis')}
            >
              Back to Analysis
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={() => {
                // Copy enhanced content to clipboard
                navigator.clipboard.writeText(enhancedContent);
              }}
            >
              Copy to Clipboard
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EnhancedJD; 