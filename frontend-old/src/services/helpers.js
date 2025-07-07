const url = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8000/';

export const getPlayerFullname = (player) => {
    if (!player) {
        return null;
    }
    return `${player.first_name} ${player.last_name}`;
}

// Helper function to get player image
export const getPlayerImage = (photoUrl) => {
  if (photoUrl) {
      if (photoUrl.startsWith('http')) {
          return photoUrl;
      }
    return url + photoUrl;
  }
  return '/assets/images/defaultPlayer.png';
};

export const getAge = (dateString) => {
    if (!dateString) {
        return null;
    }
    const today = new Date();
    const birthDate = new Date(dateString);
    let age = today.getFullYear() - birthDate.getFullYear();
    const month = today.getMonth() - birthDate.getMonth();
    if (month < 0 || (month === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

export const getCurrentDateTime = () => {
    // Take in count timezone of client
    const now = new Date();
    return now.toISOString().split('T')[0] + ' ' + now.toTimeString().split(' ')[0];
}

export const isDateInBetween = (date, startDate, endDate) => {
    return date >= startDate && date <= endDate;
}

export const getImgObj = async (photoUrl) => {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    img.src = photoUrl;
    return img;
}
