"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from "next/navigation"

export default function LoginScreen() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()

    // Sprawdzanie testowych danych logowania
    if (username === "test" && password === "test") {
      router.push("/gra")
    } else {
      setError("Nieprawidłowy login lub hasło")
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md bg-slate-800 border-slate-700">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <img src="/stylized-sword-emblem.png" alt="Master of the Sword" className="h-20 w-20" />
          </div>
          <CardTitle className="text-2xl text-yellow-400">Master of the Sword</CardTitle>
          <CardDescription className="text-gray-400">Zaloguj się, aby rozpocząć przygodę</CardDescription>
        </CardHeader>
        <form onSubmit={handleLogin}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Login</Label>
              <Input
                id="username"
                placeholder="Wprowadź login"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="bg-slate-900 border-slate-700"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Hasło</Label>
              <Input
                id="password"
                type="password"
                placeholder="Wprowadź hasło"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-slate-900 border-slate-700"
              />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
          </CardContent>
          <CardFooter>
            <Button type="submit" className="w-full">
              Zaloguj się
            </Button>
          </CardFooter>
        </form>
        <div className="p-4 text-center text-sm text-gray-400">
          <p>
            Testowe konto: login <span className="font-bold">test</span>, hasło <span className="font-bold">test</span>
          </p>
        </div>
      </Card>
    </div>
  )
}
