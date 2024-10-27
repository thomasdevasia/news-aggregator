const API_URL = "api-gateway:8000";

export async function validateToken(token: string): Promise<boolean> {
  try {
    const response = await fetch(`http://${API_URL}/validate`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await response.json();
    
    if (response.status === 200) {
      return true ;
    } else {
      return false;
    }

  } catch (error) {
    console.error("Error validating token:", error);
    return false;
  }
}
