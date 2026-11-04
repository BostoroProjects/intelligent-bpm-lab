import './style.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'Intelligent BPM Lab', description: 'Process-independent LLM experiments for FHNW BPM' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {return <html lang="en"><body>{children}</body></html>}