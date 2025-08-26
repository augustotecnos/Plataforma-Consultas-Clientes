import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Grid,
  FormControlLabel,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Menu,
  MenuItem
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Logout as LogoutIcon, 
  Visibility as VisibilityIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const ClientSearchPage = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [filters, setFilters] = useState({
    cpf: '',
    nome: '',
    cidade: '',
    uf: '',
    ativo: true
  });
  
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    pages: 0
  });
  const [exportMenuAnchor, setExportMenuAnchor] = useState(null);

  const handleFilterChange = (field) => (event) => {
    setFilters({
      ...filters,
      [field]: event.target.value
    });
  };

  const handleSwitchChange = (event) => {
    setFilters({
      ...filters,
      ativo: event.target.checked
    });
  };

  const searchClients = async (page = 1) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key] !== '' && filters[key] !== null && filters[key] !== undefined) {
          params.append(key, filters[key]);
        }
      });
      params.append('page', page);
      params.append('size', pagination.size);

      const response = await axios.get(`${API_BASE_URL}/clients/search?${params}`);
      setClients(response.data.items);
      setPagination({
        page: response.data.page,
        size: response.data.size,
        total: response.data.total,
        pages: response.data.pages
      });
    } catch (error) {
      console.error('Error searching clients:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    searchClients(1);
  };

  const handlePageChange = (event, newPage) => {
    searchClients(newPage + 1);
  };

  const handleRowClick = (clientId) => {
    navigate(`/client/${clientId}`);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleExportClick = (event) => {
    setExportMenuAnchor(event.currentTarget);
  };

  const handleExportClose = () => {
    setExportMenuAnchor(null);
  };

  const handleExport = async (format) => {
    handleExportClose();
    
    try {
      const response = await axios.post(
        `${API_BASE_URL}/clients/export`,
        {
          format,
          filters: {
            cpf: filters.cpf,
            nome: filters.nome,
            cidade: filters.cidade,
            uf: filters.uf,
            ativo: filters.ativo
          }
        },
        {
          responseType: 'blob',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const filename = `clientes_${format}_${new Date().toISOString().split('T')[0]}.${format === 'excel' ? 'xlsx' : format}`;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting clients:', error);
    }
  };

  const formatCPF = (cpf) => {
    if (!cpf) return '';
    const cleaned = cpf.replace(/\D/g, '');
    if (cleaned.length !== 11) return cpf;
    return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  };

  useEffect(() => {
    searchClients();
  }, []);

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Pesquisar Clientes
          </Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            {user?.full_name}
          </Typography>
          <IconButton color="inherit" onClick={() => navigate('/')}>
            <SearchIcon />
          </IconButton>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Filtros de Pesquisa
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="CPF"
                value={filters.cpf}
                onChange={handleFilterChange('cpf')}
                placeholder="000.000.000-00"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="Nome"
                value={filters.nome}
                onChange={handleFilterChange('nome')}
                placeholder="Nome completo ou parte"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="Cidade"
                value={filters.cidade}
                onChange={handleFilterChange('cidade')}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="UF"
                value={filters.uf}
                onChange={handleFilterChange('uf')}
                placeholder="SP"
                inputProps={{ maxLength: 2 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={filters.ativo}
                    onChange={handleSwitchChange}
                    color="primary"
                  />
                }
                label="Apenas clientes ativos"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Button
                variant="contained"
                fullWidth
                onClick={handleSearch}
                disabled={loading}
                startIcon={<SearchIcon />}
              >
                {loading ? 'Buscando...' : 'Pesquisar'}
              </Button>
            </Grid>
          </Grid>
        </Paper>

        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">
            Resultados ({pagination.total} clientes encontrados)
          </Typography>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={handleExportClick}
            disabled={clients.length === 0}
          >
            Exportar
          </Button>
          <Menu
            anchorEl={exportMenuAnchor}
            open={Boolean(exportMenuAnchor)}
            onClose={handleExportClose}
          >
            <MenuItem onClick={() => handleExport('excel')}>Exportar Excel</MenuItem>
            <MenuItem onClick={() => handleExport('csv')}>Exportar CSV</MenuItem>
            <MenuItem onClick={() => handleExport('pdf')}>Exportar PDF</MenuItem>
          </Menu>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>CPF</TableCell>
                <TableCell>Nome</TableCell>
                <TableCell>Cidade</TableCell>
                <TableCell>UF</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {clients.map((client) => (
                <TableRow 
                  key={client.id_cliente} 
                  hover 
                  sx={{ cursor: 'pointer' }}
                  onClick={() => handleRowClick(client.id_cliente)}
                >
                  <TableCell>{client.id_cliente}</TableCell>
                  <TableCell>{formatCPF(client.cpf)}</TableCell>
                  <TableCell>{client.nome_completo}</TableCell>
                  <TableCell>{client.cidade}</TableCell>
                  <TableCell>{client.uf}</TableCell>
                  <TableCell>
                    <Chip 
                      label={client.ativo ? 'Ativo' : 'Inativo'} 
                      color={client.ativo ? 'success' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton 
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRowClick(client.id_cliente);
                      }}
                      color="primary"
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[10, 25, 50]}
            component="div"
            count={pagination.total}
            rowsPerPage={pagination.size}
            page={pagination.page - 1}
            onPageChange={handlePageChange}
            labelRowsPerPage="Registros por página:"
            labelDisplayedRows={({ from, to, count }) => 
              `${from}-${to} de ${count !== -1 ? count : `mais de ${to}`}`
            }
          />
        </TableContainer>
      </Container>
    </>
  );
};

export default ClientSearchPage;
