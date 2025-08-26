import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Button,
  CircularProgress,
  Alert,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  IconButton,
} from '@mui/material';
import { ArrowBack, Edit, Download } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const ClientDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [client, setClient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchClientDetails();
  }, [id]);

  const fetchClientDetails = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/api/v1/clients/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setClient(response.data);
    } catch (err) {
      setError('Erro ao carregar detalhes do cliente');
      console.error('Error fetching client details:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    try {
      const response = await api.post('/api/v1/clients/export', {
        format,
        filters: { id_cliente: parseInt(id) }
      }, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const filename = `cliente_${client.cpf}.${format === 'excel' ? 'xlsx' : format}`;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Error exporting client:', err);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
        <Button onClick={() => navigate(-1)} sx={{ mt: 2 }}>
          Voltar
        </Button>
      </Box>
    );
  }

  if (!client) {
    return (
      <Box p={3}>
        <Alert severity="info">Cliente não encontrado</Alert>
        <Button onClick={() => navigate(-1)} sx={{ mt: 2 }}>
          Voltar
        </Button>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center" gap={2}>
          <IconButton onClick={() => navigate(-1)}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4">Detalhes do Cliente</Typography>
        </Box>
        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={() => handleExport('pdf')}
          >
            Exportar PDF
          </Button>
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={() => handleExport('excel')}
          >
            Exportar Excel
          </Button>
          <Button
            variant="contained"
            startIcon={<Edit />}
            onClick={() => navigate(`/clients/${id}/edit`)}
          >
            Editar
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Informações Pessoais */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informações Pessoais
              </Typography>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Nome Completo
                </Typography>
                <Typography variant="h6">{client.nome_completo}</Typography>
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  CPF
                </Typography>
                <Typography variant="body1">{client.cpf}</Typography>
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Data de Nascimento
                </Typography>
                <Typography variant="body1">
                  {new Date(client.data_nascimento).toLocaleDateString('pt-BR')}
                </Typography>
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Sexo
                </Typography>
                <Typography variant="body1">
                  {client.sexo === 'M' ? 'Masculino' : client.sexo === 'F' ? 'Feminino' : 'Não informado'}
                </Typography>
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Nome da Mãe
                </Typography>
                <Typography variant="body1">{client.nome_mae || 'Não informado'}</Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Status e Informações do Sistema */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informações do Sistema
              </Typography>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Status
                </Typography>
                <Chip
                  label={client.ativo ? 'Ativo' : 'Inativo'}
                  color={client.ativo ? 'success' : 'error'}
                  size="small"
                />
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  Data de Cadastro
                </Typography>
                <Typography variant="body1">
                  {new Date(client.created_at).toLocaleDateString('pt-BR')}
                </Typography>
              </Box>
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary">
                  ID do Cliente
                </Typography>
                <Typography variant="body1">{client.id_cliente}</Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Histórico de Atualizações */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Histórico de Atualizações
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Funcionalidade em desenvolvimento
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ClientDetailsPage;
