// import axios from "axios";

/**
 * Typed axios get call
 * @param url
 */
export async function axiosGetJsonData<T>(url: string): Promise<T> {
  try {
    const response = await axios.get<T>(url);
    return response.data;
  } catch (error) {
    throw new Error(`Error in 'axiosGetJsonData(${url})': ${error.message}`);
  }
}
