import { Bug, Camera, Home, Info, Maximize2, Mic, MicOff, Minimize2, Users, Video, VideoOff, X } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import { Canvas } from "@react-three/fiber";
import { Experience } from "./components/Experience";
import { Avatar } from "./components/Avatar2"; // Import Avatar

function Header({ onHomeClick, onContactClick, onAboutClick, onMansClick }: {
  onHomeClick: () => void;
  onContactClick: () => void;
  onAboutClick: () => void;
  onMansClick: () => void;
}) {
  return (
    <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <button
              onClick={onMansClick}
              className="text-2xl font-bold text-blue-600 hover:text-blue-800 transition-colors"
            >
              ORATIS
            </button>
          </div>
          <nav className="flex space-x-8">
            <button
              onClick={onHomeClick}
              className="text-gray-600 hover:text-blue-600 flex items-center gap-2"
            >
              <Home size={20} />
              Home
            </button>
            <button
              onClick={onContactClick}
              className="text-gray-600 hover:text-blue-600 flex items-center gap-2"
            >
              <Users size={20} />
              Contact
            </button>
            <button
              onClick={onAboutClick}
              className="text-gray-600 hover:text-blue-600 flex items-center gap-2"
            >
              <Info size={20} />
              About
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}

function ContactSection() {
  const developers = [
    {
      name: "Developer 1",
      role: "Frontend Developer",
      email: "dev1@mans.edu",
      photo: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop"
    },
    {
      name: "Developer 2",
      role: "Backend Developer",
      email: "dev2@mans.edu",
      photo: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop"
    },
    {
      name: "Developer 3",
      role: "ML Engineer",
      email: "dev3@mans.edu",
      photo: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop"
    },
    {
      name: "Developer 4",
      role: "UI/UX Designer",
      email: "dev4@mans.edu",
      photo: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop"
    }
  ];

  return (
    <div className="min-h-screen pt-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-3xl font-bold text-center mb-12">Our Team</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {developers.map((dev, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-6 text-center">
              <img
                src={dev.photo}
                alt={dev.name}
                className="w-32 h-32 rounded-full mx-auto mb-4 object-cover"
              />
              <h3 className="text-xl font-semibold">{dev.name}</h3>
              <p className="text-gray-600 mb-2">{dev.role}</p>
              <a href={`mailto:${dev.email}`} className="text-blue-600 hover:text-blue-800">
                {dev.email}
              </a>
            </div>
          ))}
        </div>

        {/* College Section */}
        <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center justify-center mb-8">
            <img
              src="https://images.unsplash.com/photo-1562774053-701939374585?w=1200&h=400&fit=crop"
              alt="College Banner"
              className="w-full h-48 object-cover rounded-lg"
            />
          </div>
          <div className="flex items-center justify-center mb-8">
            <img
              src="https://images.unsplash.com/photo-1599687267812-35c05ff70ee9?w=200&h=200&fit=crop"
              alt="College Logo"
              className="w-24 h-24 object-contain"
            />
          </div>
          <h2 className="text-2xl font-bold text-center mb-4">College Name</h2>
          <p className="text-gray-600 text-center">
            Add your college details and description here.
          </p>
        </div>
      </div>
    </div>
  );
}

function AboutSection() {
  return (
    <div className="min-h-screen pt-20 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-3xl font-bold text-center mb-12">About Our Tool</h2>
        
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h3 className="text-2xl font-semibold mb-4">What We Do</h3>
          <p className="text-gray-600 mb-6">
            Our AI-powered interview practice tool helps students and professionals prepare for interviews
            by providing real-time analysis of their performance. Using advanced machine learning algorithms,
            we analyze various aspects of your interview responses including language skills, body language,
            and overall presentation.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-2xl font-semibold mb-4">Technologies Used</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold mb-2">Frontend</h4>
              <ul className="list-disc list-inside text-gray-600 space-y-2">
                <li>React.js</li>
                <li>Tailwind CSS</li>
                <li>TypeScript</li>
                <li>Lucide React Icons</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-2">Backend & AI</h4>
              <ul className="list-disc list-inside text-gray-600 space-y-2">
                <li>Node.js</li>
                <li>TensorFlow.js</li>
                <li>WebRTC</li>
                <li>Natural Language Processing</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [startInterview, setStartInterview] = useState(false);
  const [endInterview, setEndInterview] = useState(false);
  const [earlyEnd, setEarlyEnd] = useState(false);
  const [isMuted, setIsMuted] = useState(true);
  const [isVideoOff, setIsVideoOff] = useState(false);
  const [showContact, setShowContact] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [resumeText, setResumeText] = useState<string | null>(null); // New state for resume text
  const [selectedFile, setSelectedFile] = useState<File | null>(null); // New state for the selected file
  const [previousState, setPreviousState] = useState<{
    startInterview: boolean;
    endInterview: boolean;
    earlyEnd: boolean;
  } | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const fullscreenContainerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const pipVideoRef = useRef<HTMLVideoElement>(null);
  const [screenDimensions, setScreenDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  
  const [score, setScore] = useState<{
    overall_score: number;
    verbal_score: number;
    non_verbal_score: number;
    filler: number;
    eye_contact: number;
    posture: number;
    vocabulary: number;
    grammar: number;
  } | null>(null);  
  const [loading, setLoading] = useState(true);

  const [avatarProps, setAvatarProps] = useState<{ playAudio: boolean; script: string }>({
    playAudio: false,
    script: "output", // Default script name
  });


  const [message, setMessage] = useState(''); // Added to store response from backend

  useEffect(() => {
    const handleResize = () => {
      setScreenDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);



    ///////////////////////////
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/get_data/'); // New endpoint for data
        console.log("response.data");
        console.log(response.data);
        const changeFlag = response.data.changeFlag === 'true';
        console.log("changeFlag");
        console.log(changeFlag);
        if (changeFlag){
          const playAudioValue = response.data.playAudio === 'true'; 
          setAvatarProps({
            playAudio: playAudioValue,
            script: response.data.script,
          }); // Assuming the backend sends { message: "your data" }
          console.log("response.data.playAudio");
          console.log(response.data.playAudio);
        }
        
        
      } catch (error) {
        console.error('Error fetching data:', error);
        
      }
    };

    useEffect(() => {
      fetchData(); // Initial fetch
  
      // Set up an interval to fetch data periodically
      const intervalId = setInterval(fetchData, 500); // Fetch data every 5 seconds (adjust as needed)
  
      // Clean up the interval when the component unmounts
      return () => clearInterval(intervalId);
    }, []);



  // Calculate scaling factors based on screen dimensions
  const getScaledSize = (baseSize: number) => {
    const scaleFactor = Math.min(
      screenDimensions.width / 1920,
      screenDimensions.height / 1080
    );
    return Math.round(baseSize * scaleFactor);
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  const toggleFullscreen = async () => {
    if (!document.fullscreenElement && fullscreenContainerRef.current) {
      await fullscreenContainerRef.current.requestFullscreen();
    } else if (document.exitFullscreen) {
      await document.exitFullscreen();
    }
  };



  useEffect(() => {
    if (endInterview && document.fullscreenElement) {
      document.exitFullscreen();
    }
  }, [endInterview]);

  // useEffect(() => {
  //   if (startInterview && !stream) {
  //     navigator.mediaDevices.getUserMedia({ video: true, audio: true })
  //       .then(mediaStream => {
  //         setStream(mediaStream);
  //         if (pipVideoRef.current) {
  //           pipVideoRef.current.srcObject = mediaStream;
  //         }
  //       })
  //       .catch(err => {
  //         console.error("Error accessing camera:", err);
  //         alert("Unable to access camera. Please check your permissions.");
  //       });
  //   }

  //   // Cleanup function
  //   return () => {
  //     if (stream) {
  //       stream.getTracks().forEach(track => track.stop());
  //     }
  //   };
  // }, [startInterview]);

  const resetStates = () => {
    setStartInterview(false);
    setEndInterview(false);
    setEarlyEnd(false);
    setIsMuted(true);
    setIsVideoOff(false);
    setShowContact(false);
    setShowAbout(false);
    setPreviousState(null);
  };

  const savePreviousState = () => {
    setPreviousState({
      startInterview,
      endInterview,
      earlyEnd
    });
  };

  const restorePreviousState = () => {
    if (previousState) {
      setStartInterview(previousState.startInterview);
      setEndInterview(previousState.endInterview);
      setEarlyEnd(previousState.earlyEnd);
      setPreviousState(null);
    }
  };

  // const handleStartInterview = () => {
  //   setStartInterview(true);
  //   setEndInterview(false);
  //   setEarlyEnd(false);

  //     // Prepare data for API call
  //     const formData = new FormData();

  //     if (selectedFile) {
  //       formData.append('resume_file', selectedFile);
  //     }
  //     if (resumeText) {
  //       formData.append('resume_text', resumeText);
  //     }

  //   axios.post('http://localhost:8000/api/start_interview/', formData, {
  //     headers: {
  //       'Content-Type': 'multipart/form-data'
  //     }
  //   }) // Replace with your actual Django endpoint and action
  //     .then(response => {
  //       if (response.data.message === "interview completed" && response.data.redirect_url) {
  //         // Redirect to the results page
  //         setStartInterview(false);
  //         setEndInterview(true);
  //         //window.location.href = response.data.redirect_url; // we dont need this line because we are not redirecting to a new page
  //       } else if (response.data.error) {
  //         // Handle errors (e.g., display an error message)
  //         console.error("Error:", response.data.error);
  //         alert("An error occurred: " + response.data.error);
  //       } else {
  //         // Handle other success messages if needed
  //         console.log("Success:", response.data.message);
  //         alert(response.data.message)
  //       }
  //     })
  //     .catch(error => {
  //       console.error('Error starting interview:', error);
  //     });
  // };
//////////////////////////////////////////////////////////////////
  const handleStartInterview = async () => {
    setStartInterview(true);
    setEndInterview(false);
    setEarlyEnd(false);

    // Prepare data for API call
    const formData = new FormData();

    if (selectedFile) {
      formData.append('resume_file', selectedFile);
    }
    if (resumeText) {
      formData.append('resume_text', resumeText);
    }

    try {
      // Make both API calls concurrently
      const [interviewResponse, nonVerbalResponse] = await Promise.all([
        axios.post('http://localhost:8000/api/start_interview/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }),
        axios.post('http://localhost:8000/api/start_non_verbal_interview/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
      ]);
      setScore(interviewResponse.data.score); // Store score in state
      setLoading(false);  // Set loading to false once we have data
      // Handle responses
      if (interviewResponse.data.message === "interview completed" && interviewResponse.data.redirect_url) {
        // Redirect to the results page
        setStartInterview(false);
        setEndInterview(true);
        //window.location.href = interviewResponse.data.redirect_url; // we dont need this line because we are not redirecting to a new page
      } else if (interviewResponse.data.error) {
        // Handle errors (e.g., display an error message)
        console.error("Error in start_interview:", interviewResponse.data.error);
        alert("An error occurred in start_interview: " + interviewResponse.data.error);
      } else {
        // Handle other success messages if needed
        console.log("Success in start_interview:", interviewResponse.data.message);
        alert(interviewResponse.data.message)
      }

      if (nonVerbalResponse.data.error) {
        console.error("Error in start_non_verbal_interview:", nonVerbalResponse.data.error);
        alert("An error occurred in start_non_verbal_interview: " + nonVerbalResponse.data.error);
      } else {
        console.log("Success in start_non_verbal_interview:", nonVerbalResponse.data.message);
        // Handle success for non-verbal if needed
      }
    } catch (error) {
      console.error('Error starting interview:', error);
      alert("An error occurred while starting the interview. Please check the console for details.");
    }
  };
//////////////////////////////////////////////////////////
  const handleEndInterview = () => {
    setEarlyEnd(true);
    setEndInterview(false);
  };

  const handleVideoToggle = () => {
    if (!isVideoOff) {
      if (window.confirm("Warning: Turning off the video will result in the soft skills section not being rated. Do you want to continue?")) {
        setIsVideoOff(true);
      }
    } else {
      setIsVideoOff(false);
    }
  };

  const handleMuteToggle = () => {
    if (!isMuted) {
      if (window.confirm("Warning: Muting the microphone will affect your language skills rating. Do you want to continue?")) {
        setIsMuted(true);
      }
    } else {
      setIsMuted(false);
    }
  };

  const handleHomeClick = () => {
    resetStates();
  };

  const handleContactClick = () => {
    if (!showContact) {
      savePreviousState();
      setShowContact(true);
      setShowAbout(false);
    } else {
      setShowContact(false);
      restorePreviousState();
    }
  };

  const handleAboutClick = () => {
    if (!showAbout) {
      savePreviousState();
      setShowAbout(true);
      setShowContact(false);
    } else {
      setShowAbout(false);
      restorePreviousState();
    }
  };

  const handleMansClick = () => {
    if (showContact) {
      setShowContact(false);
      restorePreviousState();
    } else {
      savePreviousState();
      setShowContact(true);
      setShowAbout(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResumeText(null); // Reset resumeText when a new file is selected

      const fileExtension = file.name.split('.').pop()?.toLowerCase();

      if (fileExtension === 'txt') {
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target?.result as string;
          setResumeText(text);
        };
        reader.readAsText(file);
      } else if (fileExtension === 'pdf' || fileExtension === 'docx') {
        // For PDF and DOCX, we don't read the content here.
        // We just store the file object in selectedFile.
        // The backend will handle the reading.
        console.log(`File type: ${fileExtension}. File object stored.`);
      } else {
        alert('Unsupported file type. Please select a .txt, .pdf, or .docx file.');
        setSelectedFile(null); // Clear the selected file
      }
    }
  };


  // Debug button to force show results
  const handleDebugClick = () => {
    setStartInterview(false);
    setEndInterview(true);
    setEarlyEnd(false);
  };

  if (showContact) {
    return (
      <>
        <Header
          onHomeClick={handleHomeClick}
          onContactClick={handleContactClick}
          onAboutClick={handleAboutClick}
          onMansClick={handleMansClick}
        />
        <ContactSection />
        
      </>
    );
  }

  if (showAbout) {
    return (
      <>
        <Header
          onHomeClick={handleHomeClick}
          onContactClick={handleContactClick}
          onAboutClick={handleAboutClick}
          onMansClick={handleMansClick}
        />
        <AboutSection />
        
      </>
    );
  }

  if (earlyEnd) {
    return (
      <>
        <Header
          onHomeClick={handleHomeClick}
          onContactClick={handleContactClick}
          onAboutClick={handleAboutClick}
          onMansClick={handleMansClick}
        />
        <div className="min-h-screen pt-20 bg-gray-50 flex items-center justify-center">
          <div className="max-w-2xl w-full mx-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
              <X className="w-16 h-16 text-red-600 mx-auto mb-6" />
              <h2 className="text-2xl font-bold mb-4">Interview Ended Early</h2>
              <p className="text-gray-600 mb-8">
                You ended the interview before we could complete the analysis. Would you like to try again?
              </p>
              <div className="flex justify-center gap-4">
                <button
                  onClick={handleStartInterview}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                >
                  Restart Interview
                </button>
                <button
                  onClick={handleHomeClick}
                  className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                  Back to Home
                </button>
              </div>
            </div>
          </div>
        </div>
        
      </>
    );
  }

  if (endInterview) {
    return (
      <>
        <Header
          onHomeClick={handleHomeClick}
          onContactClick={handleContactClick}
          onAboutClick={handleAboutClick}
          onMansClick={handleMansClick}
        />
        <div className="min-h-screen pt-20 bg-gray-50 p-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-center mb-12">Interview Results</h1>
            
            {/* Overall Rating */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8 text-center">
              <h2 className="text-2xl font-semibold mb-4">Overall Rating</h2>
              <div className="text-5xl font-bold text-blue-600">
                {score?.overall_score}/10  {/* Dynamic Score */}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              {/* Language Rating */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Language Skills</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Filler words</span>
                    <span className="font-semibold">{score?.filler}/10</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Vocabulary</span>
                    <span className="font-semibold">{score?.vocabulary}/10</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Grammar</span>
                    <span className="font-semibold">{score?.grammar}/10</span>
                  </div>
                </div>
              </div>

              {/* Soft Skills Rating */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Soft Skills</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Posture</span>
                    <span className="font-semibold">{score?.posture}/10</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Eye contact</span>
                    <span className="font-semibold">{score?.eye_contact}/10</span>
                  </div>
                
                </div>
              </div>
            </div>

            

            {/* Navigation Buttons */}
            <div className="flex justify-center gap-4">
              <button
                onClick={handleStartInterview}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Restart Interview
              </button>
              <button
                onClick={handleHomeClick}
                className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                Back to Home
              </button>
            </div>
          </div>
        </div>
        
      </>
    );
  }

  if (startInterview) {
    // Calculate sizes based on screen dimensions
    const buttonSize = isFullscreen ? getScaledSize(24) : 24;
    const pipWidth = isFullscreen ? getScaledSize(400) : 192; // Increased base width for fullscreen
    const pipHeight = isFullscreen ? getScaledSize(225) : 144; // Maintain 16:9 aspect ratio
    const controlsPadding = isFullscreen ? getScaledSize(16) : 12;
    const modelScale = isFullscreen ? `scale(${getScaledSize(150) / 100})` : 'scale(1)';

    return (
      <>
        <Header
          onHomeClick={handleHomeClick}
          onContactClick={handleContactClick}
          onAboutClick={handleAboutClick}
          onMansClick={handleMansClick}
        />
        <div className="min-h-screen pt-20 bg-gray-900 p-4">
          <div 
            ref={fullscreenContainerRef}
            className={`relative ${isFullscreen ? 'fixed inset-0 z-50 bg-gray-900' : 'max-w-4xl mx-auto'}`}
          >
            <div className={`${isFullscreen ? 'h-full p-4 flex flex-col' : ''}`}>
              <div className={`relative ${isFullscreen ? 'flex-grow' : 'aspect-video'} bg-gradient-to-b from-gray-800 to-gray-900 rounded-lg overflow-hidden ${isFullscreen ? 'mb-6' : 'mb-4'}`}>
                {/* Mock 3D AI Model */}
                {!isVideoOff && (
                  <div className="absolute inset-0 flex items-center justify-center">
                     <Canvas shadows camera={{ position: [0, 0, 8], fov: 42 }}>
                      <color attach="background" args={["#ececec"]} />
                      <Experience />
                      <Avatar
                        position={[0, -4, 5]} scale={2.8}
                        playAudio={avatarProps.playAudio}
                        script={avatarProps.script}
                      />
                    </Canvas>
                    {/* <AIModel isVideoOff={isVideoOff} modelScale={modelScale} /> */}
                  </div>
                )}
                {isVideoOff && (
                  <div className="absolute inset-0 flex items-center justify-center bg-gray-800">
                    <Camera className={`w-${buttonSize} h-${buttonSize} text-gray-600`} />
                  </div>
                )}

                {/* Picture-in-Picture User Camera */}
                

                {/* Fullscreen Toggle Button */}
                <button
                  onClick={toggleFullscreen}
                  className="absolute top-4 right-4 p-2 rounded-full bg-gray-800 hover:bg-gray-700 text-white transition-colors z-[51] cursor-pointer"
                  style={{ 
                    WebkitAppearance: 'none',
                    padding: `${controlsPadding}px`
                  }}
                >
                  {isFullscreen ? (
                    <Minimize2 size={buttonSize * 0.8} />
                  ) : (
                    <Maximize2 size={buttonSize * 0.8} />
                  )}
                </button>
              </div>

              {/* Controls */}
              <div 
                className={`flex justify-center gap-4 ${isFullscreen ? 'pb-4' : ''} relative z-[52]`}
                style={{ gap: `${controlsPadding * 2}px` }}
              >
                <button
                  onClick={handleMuteToggle}
                  className="rounded-full bg-gray-800 hover:bg-gray-700 text-white transition-colors"
                  style={{ padding: `${controlsPadding}px` }}
                >
                  {isMuted ? (
                    <MicOff size={buttonSize} />
                  ) : (
                    <Mic size={buttonSize} />
                  )}
                </button>
                <button
                  onClick={handleVideoToggle}
                  className="rounded-full bg-gray-800 hover:bg-gray-700 text-white transition-colors"
                  style={{ padding: `${controlsPadding}px` }}
                >
                  {isVideoOff ? (
                    <VideoOff size={buttonSize} />
                  ) : (
                    <Video size={buttonSize} />
                  )}
                </button>
                <button
                  onClick={handleEndInterview}
                  className="rounded-full bg-red-600 hover:bg-red-700 text-white flex items-center gap-2 transition-colors"
                  style={{ 
                    padding: `${controlsPadding}px ${controlsPadding * 2}px`,
                    gap: `${controlsPadding}px`
                  }}
                >
                  <X size={buttonSize} />
                  <span style={{ fontSize: `${buttonSize * 0.75}px` }}>
                    End Interview
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
       
      </>
    );
  }

  return (
    <>
      <Header
        onHomeClick={handleHomeClick}
        onContactClick={handleContactClick}
        onAboutClick={handleAboutClick}
        onMansClick={handleMansClick}
      />
      <div 
        className="min-h-screen pt-20 flex items-center justify-center p-4 bg-cover bg-center"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=1920&h=1080&fit=crop")',
          backgroundBlendMode: 'overlay',
          backgroundColor: 'rgba(255, 255, 255, 0.9)'
        }}
      >
        <div className="max-w-2xl w-full">
          <div className="bg-white bg-opacity-95 backdrop-blur-sm rounded-2xl shadow-xl p-8 text-center">
            <Camera className="w-16 h-16 text-blue-600 mx-auto mb-6" />
            <h1 className="text-3xl font-bold mb-4">AI Interview Practice</h1>
            <p className="text-gray-600 mb-8">
              Practice your interview skills with our AI-powered analysis tool. Get instant feedback on your language skills,
              body language, and overall performance. Our advanced AI will analyze your video responses and provide detailed
              suggestions for improvement.
            </p>
            {/* File Upload Input */}
            <div className="mb-4">
            <input
              type="file"
              id="resume-upload" // Add an ID
              accept=".txt,.pdf,.docx" // Specify accepted file types
              onChange={handleFileChange}
              className="hidden"
            />
            <label
                htmlFor="resume-upload" // Link the label to the input
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer"
              >
                Choose File
              </label>
              </div>
            <button
              onClick={handleStartInterview}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Start Interview Now
            </button>
          </div>
        </div>
      </div>
      
    </>
  );
}

export default App;