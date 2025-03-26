import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
          }}
        >
          JD Analyzer
        </Typography>
        <Box>
          <Button
            color="inherit"
            component={RouterLink}
            to="/"
          >
            Input
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/analysis"
          >
            Analysis
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/enhanced"
          >
            Enhanced JD
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 