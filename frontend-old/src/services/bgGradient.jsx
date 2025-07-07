import { useEffect, useState } from 'react';
import ColorThief from 'colorthief';
import { getImgObj } from 'services/helpers.js';

export const getDominantColor = async (image, defaultColor) => {
  const colorThief = new ColorThief();

  if (!image) {
    return defaultColor;
  }

  return new Promise((resolve) => {
    image.onload = () => {
      try {
        const dominantColor = colorThief.getColor(image);
        resolve(dominantColor);
      } catch {
        resolve(defaultColor);
      }
    };
    image.onerror = () => resolve(defaultColor);
  });
};

export const useBackgroundGradient = (selectedPlayers, players, matchType) => {
  const [backgroundGradient, setBackgroundGradient] = useState('white');

  useEffect(() => {
    const updateGradient = async () => {
      const defaultColor = [255, 255, 255]; // Default white background

      const colors = await Promise.all(
        Object.values(selectedPlayers).map(async (playerId) => {
          if (!playerId) return defaultColor;
          const player = players.find((p) => p.id === Number(playerId));
          const img = await getImgObj(player?.photo);
          return getDominantColor(img, defaultColor);
        })
      );

      if (matchType === 'singles') {
        setBackgroundGradient(
          `linear-gradient(to right, rgba(${colors[0].join(',')}, 0.8), rgba(${colors[1].join(',')}, 0.8))`
        );
      } else {
        setBackgroundGradient(
          `linear-gradient(135deg, rgba(${colors[0].join(',')}, 1), rgba(${colors[0].join(',')}, 0) 70.71%),
           linear-gradient(45deg, rgba(${colors[1].join(',')}, 1), rgba(${colors[1].join(',')}, 0) 70.71%),
           linear-gradient(225deg, rgba(${colors[2].join(',')}, 1), rgba(${colors[2].join(',')}, 0) 70.71%),
           linear-gradient(315deg, rgba(${colors[3].join(',')}, 1), rgba(${colors[3].join(',')}, 0) 70.71%)`
        );
      }
    };

    updateGradient();
  }, [selectedPlayers, players, matchType]);

  return backgroundGradient;
};