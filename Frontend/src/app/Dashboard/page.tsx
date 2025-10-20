import Image from "next/image";
import Sidebar from "@/components/sidebar"
import Dashboard from "@/components/dashboard"

export default function Home() {
  return (
    <>
      <Sidebar/>
      <Dashboard/>
    </>
  );
}
