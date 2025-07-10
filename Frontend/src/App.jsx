import './App.css'
import { ArtistTools } from './modules/generalComponents/components/ArtistTools'
import { Nav } from './modules/generalComponents/components/Nav'
import { Library } from './modules/library/components/Library'

function App() {
  return (
    <>
      <div className="navContainer">
        <Nav />
      </div>
      <div className="generalContent">
        <Library />
        <ArtistTools />
      </div>
    </>
  )
}

export default App
