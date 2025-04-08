import { FlaskRoundIcon as Flask } from "lucide-react"

const Tavern = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-8">Welcome to the Tavern!</h1>
      <Flask className="h-16 w-16 mb-4 text-green-400" />
      <p className="text-lg">Pull up a chair and enjoy the atmosphere.</p>
    </div>
  )
}

export default Tavern
