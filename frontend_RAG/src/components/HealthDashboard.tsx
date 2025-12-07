import React, { useState, useEffect } from "react";
import { API_ENDPOINTS } from "../config";

interface HealthStatus {
  status: string;
  timestamp: string;
  uptime_seconds: number;
  services: {
    database: any;
    cache: any;
    llm: any;
  };
  metrics: {
    requests: {
      total: number;
      success: number;
      errors: number;
      error_rate: number;
      success_rate: number;
    };
  };
  alerts: {
    recent_count: number;
    critical_count: number;
    error_count: number;
    recent: Array<{
      title: string;
      level: string;
      timestamp: string;
    }>;
  };
}

const HealthDashboard: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch(API_ENDPOINTS.health.basic);
        if (!response.ok) {
          throw new Error("Erreur lors de la récupération de la santé");
        }
        const data = await response.json();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 30000); // Rafraîchir toutes les 30s

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "text-green-500";
      case "degraded":
        return "text-yellow-500";
      case "unhealthy":
      case "critical":
        return "text-red-500";
      default:
        return "text-gray-500";
    }
  };

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days}d ${hours}h ${minutes}m`;
  };

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse">Chargement du dashboard de santé...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <div className="text-red-500">Erreur: {error}</div>
      </div>
    );
  }

  if (!health) {
    return null;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Dashboard de Santé</h1>

      {/* Statut global */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Statut Global</h2>
            <p className={`text-2xl font-bold ${getStatusColor(health.status)}`}>
              {health.status.toUpperCase()}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">Uptime</p>
            <p className="text-lg font-semibold">{formatUptime(health.uptime_seconds)}</p>
          </div>
        </div>
      </div>

      {/* Services */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Database */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 className="font-semibold mb-2">Base de données</h3>
          <p className={`text-sm ${getStatusColor(health.services.database.status)}`}>
            {health.services.database.status}
          </p>
          {health.services.database.response_time_ms && (
            <p className="text-xs text-gray-500 mt-1">
              {health.services.database.response_time_ms}ms
            </p>
          )}
        </div>

        {/* Cache */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 className="font-semibold mb-2">Cache Redis</h3>
          <p className={`text-sm ${getStatusColor(health.services.cache.status)}`}>
            {health.services.cache.status}
          </p>
          {health.services.cache.response_time_ms && (
            <p className="text-xs text-gray-500 mt-1">
              {health.services.cache.response_time_ms}ms
            </p>
          )}
        </div>

        {/* LLM */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 className="font-semibold mb-2">LLM (Ollama)</h3>
          <p className={`text-sm ${getStatusColor(health.services.llm.status)}`}>
            {health.services.llm.status}
          </p>
          {health.services.llm.response_time_ms && (
            <p className="text-xs text-gray-500 mt-1">
              {health.services.llm.response_time_ms}ms
            </p>
          )}
        </div>
      </div>

      {/* Métriques */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Métriques</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div>
            <p className="text-sm text-gray-500">Requêtes totales</p>
            <p className="text-2xl font-bold">{health.metrics.requests.total}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Succès</p>
            <p className="text-2xl font-bold text-green-500">
              {health.metrics.requests.success}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Erreurs</p>
            <p className="text-2xl font-bold text-red-500">
              {health.metrics.requests.errors}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Taux d'erreur</p>
            <p className="text-2xl font-bold">
              {(health.metrics.requests.error_rate * 100).toFixed(1)}%
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Taux de succès</p>
            <p className="text-2xl font-bold text-green-500">
              {(health.metrics.requests.success_rate * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      {/* Alertes */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Alertes Récentes</h2>
        <div className="space-y-2">
          {health.alerts.recent_count === 0 ? (
            <p className="text-gray-500">Aucune alerte récente</p>
          ) : (
            <>
              <div className="flex gap-4 mb-4">
                <span className="text-sm">
                  Total: <strong>{health.alerts.recent_count}</strong>
                </span>
                {health.alerts.critical_count > 0 && (
                  <span className="text-sm text-red-500">
                    Critique: <strong>{health.alerts.critical_count}</strong>
                  </span>
                )}
                {health.alerts.error_count > 0 && (
                  <span className="text-sm text-orange-500">
                    Erreur: <strong>{health.alerts.error_count}</strong>
                  </span>
                )}
              </div>
              <div className="space-y-2">
                {health.alerts.recent.map((alert, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded border-l-4 ${
                      alert.level === "critical"
                        ? "border-red-500 bg-red-50 dark:bg-red-900/20"
                        : alert.level === "error"
                        ? "border-orange-500 bg-orange-50 dark:bg-orange-900/20"
                        : alert.level === "warning"
                        ? "border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20"
                        : "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                    }`}
                  >
                    <div className="flex justify-between">
                      <p className="font-semibold">{alert.title}</p>
                      <p className="text-xs text-gray-500">
                        {new Date(alert.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                      {alert.level.toUpperCase()}
                    </p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default HealthDashboard;

