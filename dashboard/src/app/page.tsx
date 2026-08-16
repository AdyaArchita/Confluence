"use client";

import React, { useEffect, useState } from "react";
import { 
  Users, AlertCircle, MessageSquare, LayoutDashboard, Settings, Radio, 
  MessageCircle, Mail, Hash, AlertOctagon
} from "lucide-react";

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/stats")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error(err));
  }, []);

  const getChannelIcon = (channel: string) => {
    switch(channel?.toLowerCase()) {
      case "telegram": return <MessageCircle className="w-3.5 h-3.5 text-dashboard-muted" />;
      case "discord": return <Hash className="w-3.5 h-3.5 text-dashboard-muted" />;
      case "email": return <Mail className="w-3.5 h-3.5 text-dashboard-muted" />;
      default: return <MessageSquare className="w-3.5 h-3.5 text-dashboard-muted" />;
    }
  };

  return (
    <div 
      className="flex h-screen bg-dashboard-background text-dashboard-text antialiased overflow-hidden selection:bg-dashboard-accent/20 selection:text-dashboard-accent"
      style={{ fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif' }}
    >
      
      {/* Sidebar - Fixed */}
      <aside className="w-[240px] flex-shrink-0 border-r border-dashboard-border bg-dashboard-card flex flex-col h-full">
        <div className="px-5 py-6">
          <h2 className="text-sm font-semibold text-dashboard-text tracking-tight">Confluence</h2>
          <p className="text-[11px] text-dashboard-muted mt-0.5 font-medium">Caspian Event Coordinator</p>
        </div>
        
        <nav className="flex-1 px-3 space-y-0.5 mt-2 overflow-y-auto">
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded bg-dashboard-accent/10 text-dashboard-accent text-sm font-medium">
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </a>
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded hover:bg-dashboard-background text-dashboard-muted hover:text-dashboard-text text-sm font-medium transition-none">
            <Users className="w-4 h-4" /> Attendees & RSVPs
          </a>
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded hover:bg-dashboard-background text-dashboard-muted hover:text-dashboard-text text-sm font-medium transition-none">
            <AlertCircle className="w-4 h-4" /> Escalations
          </a>
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded hover:bg-dashboard-background text-dashboard-muted hover:text-dashboard-text text-sm font-medium transition-none">
            <MessageSquare className="w-4 h-4" /> Multi-Channel Feed
          </a>
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded hover:bg-dashboard-background text-dashboard-muted hover:text-dashboard-text text-sm font-medium transition-none">
            <Radio className="w-4 h-4" /> Broadcast Center
          </a>
        </nav>
        
        <div className="p-3 border-t border-dashboard-border">
          <a href="#" className="flex items-center gap-2.5 px-2.5 py-1.5 rounded hover:bg-dashboard-background text-dashboard-muted hover:text-dashboard-text text-sm font-medium transition-none">
            <Settings className="w-4 h-4" /> Settings
          </a>
        </div>
      </aside>

      {/* Main Content Area - Scrollable */}
      <main className="flex-1 flex flex-col min-w-0 h-full bg-dashboard-background">
        {/* Header - Fixed at top of main content */}
        <header className="h-14 flex-shrink-0 border-b border-dashboard-border bg-dashboard-card flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-3">
            <h1 className="text-sm font-semibold text-dashboard-text">Dashboard</h1>
            <div className="h-4 w-px bg-dashboard-border mx-2"></div>
            <div className="flex items-center gap-2 text-xs text-dashboard-muted font-medium">
              <span className="w-2 h-2 rounded-full bg-dashboard-success"></span>
              Caspian Gateway: Connected
            </div>
          </div>
          <button className="bg-dashboard-accent hover:opacity-90 text-white text-xs font-medium px-4 py-1.5 rounded flex items-center gap-1.5 shadow-none transition-none">
            <Radio className="w-3.5 h-3.5" /> New Broadcast
          </button>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-[1200px] mx-auto space-y-6">
            
            {/* Metrics Row (4 cards) */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Total RSVPs */}
              <div className="bg-dashboard-card border border-dashboard-border rounded p-5 flex flex-col justify-between h-[112px]">
                <span className="text-[12px] font-medium text-dashboard-muted">Total RSVPs</span>
                <div>
                  <div className="text-2xl font-semibold text-dashboard-text">{stats?.total_rsvps || 0}</div>
                  <div className="text-[11px] text-dashboard-muted mt-1">Confirmed attendees</div>
                </div>
              </div>
              
              {/* Escalations */}
              <div className="bg-dashboard-card border border-dashboard-border rounded p-5 flex flex-col justify-between h-[112px]">
                <span className="text-[12px] font-medium text-dashboard-muted">Open Escalations</span>
                <div>
                  <div className="text-2xl font-semibold text-dashboard-warning">{stats?.escalations_count || 0}</div>
                  <div className="text-[11px] text-dashboard-muted mt-1">Requires human attention</div>
                </div>
              </div>

              {/* Active Channels */}
              <div className="bg-dashboard-card border border-dashboard-border rounded p-5 flex flex-col justify-between h-[112px]">
                <span className="text-[12px] font-medium text-dashboard-muted">Active Channels</span>
                <div>
                  <div className="text-2xl font-semibold text-dashboard-text">{stats?.active_channels?.length || 0}</div>
                  <div className="flex gap-1.5 mt-1.5">
                    {(stats?.active_channels || []).map((ch: string) => (
                      <span key={ch} title={ch}>{getChannelIcon(ch)}</span>
                    ))}
                    {!stats?.active_channels?.length && <span className="text-[11px] text-dashboard-muted">None</span>}
                  </div>
                </div>
              </div>

              {/* T-Shirt Summary */}
              <div className="bg-dashboard-card border border-dashboard-border rounded p-5 flex flex-col justify-between h-[112px]">
                <span className="text-[12px] font-medium text-dashboard-muted">T-Shirt Summary</span>
                <div className="flex gap-4 items-end mt-1">
                  {["S", "M", "L", "XL"].map(size => (
                    <div key={size} className="flex flex-col items-center gap-0.5">
                      <span className="text-[13px] font-semibold text-dashboard-text">{stats?.tshirt_counts?.[size] || 0}</span>
                      <span className="text-[10px] text-dashboard-muted">{size}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Lower Section (Escalations left, Attendees right) */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              
              {/* Escalation Queue (Col span 4) */}
              <div className="lg:col-span-4 bg-dashboard-card border border-dashboard-border rounded flex flex-col overflow-hidden max-h-[600px]">
                <div className="px-5 py-4 border-b border-dashboard-border flex items-center gap-2 bg-dashboard-card">
                  <AlertOctagon className="w-4 h-4 text-dashboard-error" />
                  <h3 className="text-sm font-semibold text-dashboard-text">Escalation Queue</h3>
                </div>
                
                <div className="flex-1 overflow-y-auto p-3 space-y-3">
                  {stats?.attendees?.filter((a: any) => a.escalated).length === 0 || !stats ? (
                    <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                      <span className="w-2.5 h-2.5 rounded-full bg-dashboard-success shadow-none"></span>
                      <p className="text-xs text-dashboard-muted font-medium">Inbox zero! No open escalations.</p>
                    </div>
                  ) : (
                    stats?.attendees?.filter((a: any) => a.escalated).map((user: any) => (
                      <div key={user.id} className="p-4 rounded border border-dashboard-border bg-dashboard-card flex flex-col gap-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {getChannelIcon(user.channel)}
                            <span className="text-xs font-semibold text-dashboard-text">{user.name || user.id}</span>
                          </div>
                          <span className="text-[10px] text-dashboard-muted font-medium">
                            {new Date(user.registered_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                          </span>
                        </div>
                        <p className="text-xs text-dashboard-muted line-clamp-2 leading-relaxed">
                          User requires manual intervention regarding their RSVP or event details.
                        </p>
                        <button className="mt-2 w-full bg-dashboard-background border border-dashboard-border hover:bg-gray-100 text-dashboard-text text-xs font-medium py-1.5 rounded transition-none">
                          Respond
                        </button>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Registered Attendees (Col span 8) */}
              <div className="lg:col-span-8 bg-dashboard-card border border-dashboard-border rounded flex flex-col overflow-hidden max-h-[600px]">
                <div className="px-5 py-4 border-b border-dashboard-border bg-dashboard-card">
                  <h3 className="text-sm font-semibold text-dashboard-text">Registered Attendees</h3>
                </div>
                
                <div className="flex-1 overflow-y-auto">
                  <table className="w-full text-left border-collapse">
                    <thead className="sticky top-0 bg-dashboard-background z-10 border-b border-dashboard-border">
                      <tr>
                        <th className="px-5 py-3 text-[12px] font-medium text-dashboard-muted">Name</th>
                        <th className="px-5 py-3 text-[12px] font-medium text-dashboard-muted">Channel</th>
                        <th className="px-5 py-3 text-[12px] font-medium text-dashboard-muted">Status</th>
                        <th className="px-5 py-3 text-[12px] font-medium text-dashboard-muted text-right">Registered</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-dashboard-border">
                      {stats?.attendees?.length === 0 || !stats ? (
                        <tr>
                          <td colSpan={4} className="px-5 py-12 text-center text-xs text-dashboard-muted font-medium">
                            Waiting for attendees to RSVP via the AI agent...
                          </td>
                        </tr>
                      ) : (
                        stats?.attendees?.map((user: any) => (
                          <tr key={user.id} className="hover:bg-dashboard-background transition-none">
                            <td className="px-5 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-3">
                                <div className="w-6 h-6 rounded-full bg-dashboard-background border border-dashboard-border flex items-center justify-center text-[10px] text-dashboard-text font-medium">
                                  {user.name?.charAt(0)?.toUpperCase() || '?'}
                                </div>
                                <span className="text-xs font-medium text-dashboard-text">{user.name || user.id}</span>
                              </div>
                            </td>
                            <td className="px-5 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-2 text-dashboard-muted">
                                {getChannelIcon(user.channel)}
                                <span className="capitalize text-xs font-medium">{user.channel || "Unknown"}</span>
                              </div>
                            </td>
                            <td className="px-5 py-4 whitespace-nowrap">
                              {user.rsvp?.status === "confirmed" ? (
                                <div className="flex items-center gap-1.5 text-dashboard-text text-xs font-medium">
                                  <span className="w-2 h-2 rounded-full bg-dashboard-success"></span>
                                  Confirmed
                                </div>
                              ) : (
                                <div className="flex items-center gap-1.5 text-dashboard-muted text-xs font-medium">
                                  <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                                  Pending
                                </div>
                              )}
                            </td>
                            <td className="px-5 py-4 whitespace-nowrap text-right text-xs text-dashboard-muted font-medium">
                              {new Date(user.registered_at).toLocaleDateString()}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
