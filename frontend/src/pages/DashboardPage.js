import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  AppBar,
  Toolbar,
  IconButton
} from '@mui/material';
import {
  Search as SearchIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const cards = [
    {
      title: 'Pesquisar Clientes',
      description: 'Busque clientes por CPF, nome, cidade e outros filtros',
      icon: <SearchIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/search'),
      color: '#1976d2'
    },
    {
      title: 'Relatórios',
      description: 'Gere relatórios e exporte dados em Excel, PDF ou CSV',
      icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/search'),
      color: '#388e3c'
    },
    {
      title: 'Gestão de Usuários',
      description: 'Gerencie usuários e permissões do sistema',
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      action: () => alert('Funcionalidade em desenvolvimento'),
      color: '#f57c00'
    },
    {
      title: 'Configurações',
      description: 'Configure preferências e parâmetros do sistema',
      icon: <SettingsIcon sx={{ fontSize: 40 }} />,
      action: () => alert('Funcionalidade em desenvolvimento'),
      color: '#7b1fa2'
    }
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Sistema de Gestão de Clientes
          </Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            Olá, {user?.full_name || 'Usuário'}
          </Typography>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Bem-vindo ao sistema de gestão de clientes. Selecione uma opção abaixo para começar.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {cards.map((card, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ color: card.color, mb: 2 }}>
                    {card.icon}
                  </Box>
                  <Typography gutterBottom variant="h5" component="h2">
                    {card.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {card.description}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="large" 
                    fullWidth 
                    variant="contained" 
                    onClick={card.action}
                    sx={{ bgcolor: card.color }}
                  >
                    Acessar
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Versão 1.0.0 | Desenvolvido para atender às necessidades da Maria, Analista de Atendimento
          </Typography>
        </Box>
      </Container>
    </>
  );
};

export default DashboardPage;
