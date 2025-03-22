// src/components/GLBStructureReader.tsx
import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

interface GLBStructureReaderProps {
  modelPath: string;
}

interface NodeInfo {
  name: string;
  type: string;
  userData?: any;
  children?: NodeInfo[];
}

const GLBStructureReader: React.FC<GLBStructureReaderProps> = ({ modelPath }) => {
  const [structure, setStructure] = useState<NodeInfo | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loader = new GLTFLoader();

    loader.load(
      modelPath,
      (gltf) => {
        const model = gltf.scene;
        const rootStructure = buildStructure(model);
        setStructure(rootStructure);
      },
      undefined,
      (error) => {
        console.error('An error happened:', error);
      }
    );
  }, [modelPath]);

  const buildStructure = (object: THREE.Object3D): NodeInfo => {
    const nodeInfo: NodeInfo = {
      name: object.name,
      type: object.type,
    };

    if (Object.keys(object.userData).length > 0) {
      nodeInfo.userData = object.userData;
    }

    if (object.children.length > 0) {
      nodeInfo.children = object.children.map(buildStructure);
    }

    return nodeInfo;
  };

  const renderStructure = (node: NodeInfo, level: number = 0): JSX.Element => {
    const indent = '  '.repeat(level);
    return (
      <div key={node.name + level} style={{ marginLeft: `${level * 20}px` }}>
        <div>
          {indent}
          {node.name} ({node.type})
          {node.userData && (
            <pre style={{ display: 'inline', whiteSpace: 'pre-wrap' }}>
              : {JSON.stringify(node.userData, null, 2)}
            </pre>
          )}
        </div>
        {node.children &&
          node.children.map((child) => renderStructure(child, level + 1))}
      </div>
    );
  };

  return (
    <div ref={containerRef}>
      <h2>GLB File Structure:</h2>
      {structure ? (
        <div style={{ fontFamily: 'monospace' }}>
          {renderStructure(structure)}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default GLBStructureReader;
