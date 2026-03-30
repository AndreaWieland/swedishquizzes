import React, { useState, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  ActivityIndicator,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { useApi } from "@/lib/ApiContext";
import { TopicStats } from "@/lib/types";

interface StatsRow {
  name: string;
  stats: TopicStats;
}

export default function StatsScreen() {
  const { api } = useApi();
  const [data, setData] = useState<StatsRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(
    async (isRefresh = false) => {
      if (!api) return;
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      setError(null);
      try {
        const stats = await api.getStats();
        const rows: StatsRow[] = Object.entries(stats).map(
          ([name, s]) => ({ name, stats: s })
        );
        rows.sort((a, b) => a.name.localeCompare(b.name));
        setData(rows);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Unknown error");
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [api]
  );

  useFocusEffect(
    useCallback(() => {
      fetchStats();
    }, [fetchStats])
  );

  if (!api) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyText}>Please configure the API URL first.</Text>
      </View>
    );
  }

  if (loading && !refreshing) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  const formatName = (name: string) =>
    name
      .split("_")
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(" ");

  const renderItem = ({ item }: { item: StatsRow }) => {
    const { stats } = item;
    const accuracyPct = Math.round(stats.accuracy * 100);

    return (
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Text style={styles.topicName}>{formatName(item.name)}</Text>
          <View
            style={[
              styles.accuracyBadge,
              accuracyPct >= 80
                ? styles.accuracyGood
                : accuracyPct >= 50
                ? styles.accuracyMedium
                : styles.accuracyLow,
            ]}
          >
            <Text
              style={[
                styles.accuracyText,
                accuracyPct >= 80
                  ? styles.accuracyTextGood
                  : accuracyPct >= 50
                  ? styles.accuracyTextMedium
                  : styles.accuracyTextLow,
              ]}
            >
              {accuracyPct}%
            </Text>
          </View>
        </View>

        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.words_seen}</Text>
            <Text style={styles.statLabel}>Words seen</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.total_asked}</Text>
            <Text style={styles.statLabel}>Questions</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.total_correct}</Text>
            <Text style={styles.statLabel}>Correct</Text>
          </View>
        </View>

        <View style={styles.progressBarBg}>
          <View
            style={[
              styles.progressBarFill,
              { width: `${accuracyPct}%` },
              accuracyPct >= 80
                ? styles.barGood
                : accuracyPct >= 50
                ? styles.barMedium
                : styles.barLow,
            ]}
          />
        </View>
      </View>
    );
  };

  return (
    <FlatList
      style={styles.container}
      contentContainerStyle={styles.listContent}
      data={data}
      keyExtractor={(item) => item.name}
      renderItem={renderItem}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={() => fetchStats(true)}
          tintColor="#2563eb"
        />
      }
      ListEmptyComponent={
        <View style={styles.emptyContainer}>
          {error ? (
            <Text style={styles.errorText}>{error}</Text>
          ) : (
            <Text style={styles.emptyText}>
              No stats yet. Start learning and quizzing to see your progress!
            </Text>
          )}
        </View>
      }
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  listContent: {
    padding: 20,
    paddingBottom: 40,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f8f9fa",
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: 14,
    padding: 18,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  topicName: {
    fontSize: 17,
    fontWeight: "700",
    color: "#1e293b",
  },
  accuracyBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  accuracyGood: {
    backgroundColor: "#f0fdf4",
  },
  accuracyMedium: {
    backgroundColor: "#fffbeb",
  },
  accuracyLow: {
    backgroundColor: "#fef2f2",
  },
  accuracyText: {
    fontSize: 14,
    fontWeight: "700",
  },
  accuracyTextGood: {
    color: "#16a34a",
  },
  accuracyTextMedium: {
    color: "#d97706",
  },
  accuracyTextLow: {
    color: "#dc2626",
  },
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginBottom: 14,
  },
  statItem: {
    alignItems: "center",
  },
  statValue: {
    fontSize: 20,
    fontWeight: "700",
    color: "#1e293b",
  },
  statLabel: {
    fontSize: 12,
    color: "#94a3b8",
    marginTop: 2,
  },
  progressBarBg: {
    height: 6,
    backgroundColor: "#e2e8f0",
    borderRadius: 3,
    overflow: "hidden",
  },
  progressBarFill: {
    height: 6,
    borderRadius: 3,
  },
  barGood: {
    backgroundColor: "#16a34a",
  },
  barMedium: {
    backgroundColor: "#d97706",
  },
  barLow: {
    backgroundColor: "#dc2626",
  },
  emptyContainer: {
    padding: 40,
    alignItems: "center",
  },
  emptyText: {
    fontSize: 16,
    color: "#64748b",
    textAlign: "center",
    lineHeight: 24,
  },
  errorText: {
    fontSize: 14,
    color: "#dc2626",
  },
});
