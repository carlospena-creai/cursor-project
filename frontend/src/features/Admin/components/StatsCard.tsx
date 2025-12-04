/**
 * StatsCard Component
 *
 * Componente para mostrar una tarjeta de estadística en el dashboard.
 */
import React from "react";
import { Card, Statistic, Spin } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";

interface StatsCardProps {
  title: string;
  value: number | string;
  prefix?: string;
  suffix?: string;
  loading?: boolean;
  trend?: "up" | "down";
  trendValue?: number;
  icon?: React.ReactNode;
  color?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  suffix,
  loading = false,
  trend,
  trendValue,
  icon,
  color = "#1890ff",
}) => {
  return (
    <Card>
      <Spin spinning={loading}>
        <Statistic
          title={title}
          value={value}
          prefix={icon}
          suffix={suffix}
          valueStyle={{ color }}
        />
        {trend && trendValue !== undefined && (
          <div style={{ marginTop: 8, fontSize: 12, color: "#8c8c8c" }}>
            {trend === "up" ? (
              <ArrowUpOutlined style={{ color: "#52c41a" }} />
            ) : (
              <ArrowDownOutlined style={{ color: "#ff4d4f" }} />
            )}{" "}
            {trendValue}% desde el mes pasado
          </div>
        )}
      </Spin>
    </Card>
  );
};
