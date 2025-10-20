import { Twilio } from 'twilio';

const twilioClient = new Twilio(
  process.env.TWILIO_ACCOUNT_SID!,
  process.env.TWILIO_AUTH_TOKEN!
);
const twilioWhatsAppNumber = process.env.TWILIO_WHATSAPP_NUMBER!;

export class WhatsAppService {
  /**
   * Send a WhatsApp message to a user by username
   * TODO: Implement Firestore user lookup
   */
  static async sendMessageByUsername(
    username: string,
    message: string
  ): Promise<boolean> {
    try {
      // TODO: Replace with Firestore query
      // Find the user by username
      const user = null; // Replace with Firestore query

      if (!user) {
        console.error(`User not found: ${username}`);
        return false;
      }

      // TODO: Access user.whatsappNumber from Firestore document
      const whatsappNumber = null; // Replace with user.whatsappNumber

      // Check if user has WhatsApp linked
      if (!whatsappNumber) {
        console.log(`User ${username} doesn't have WhatsApp linked`);
        return false;
      }

      // Send WhatsApp message
      await twilioClient.messages.create({
        from: twilioWhatsAppNumber,
        to: `whatsapp:${whatsappNumber}`,
        body: message,
      });

      console.log(`WhatsApp message sent to ${username}`);
      return true;
    } catch (error) {
      console.error('Error sending WhatsApp message:', error);
      return false;
    }
  }

  /**
   * Send a WhatsApp message to a phone number directly
   */
  static async sendMessageToNumber(
    phoneNumber: string,
    message: string
  ): Promise<boolean> {
    try {
      // Send WhatsApp message
      await twilioClient.messages.create({
        from: twilioWhatsAppNumber,
        to: `whatsapp:${phoneNumber}`,
        body: message,
      });

      console.log(`WhatsApp message sent to ${phoneNumber}`);
      return true;
    } catch (error) {
      console.error('Error sending WhatsApp message:', error);
      return false;
    }
  }

  /**
   * Check if a user has WhatsApp linked
   * TODO: Implement Firestore user lookup
   */
  static async hasWhatsAppLinked(username: string): Promise<boolean> {
    try {
      // TODO: Replace with Firestore query
      const user = null; // Replace with Firestore query

      // TODO: Access user.whatsappNumber from Firestore document
      return false; // Replace with !!user?.whatsappNumber
    } catch (error) {
      console.error('Error checking WhatsApp link status:', error);
      return false;
    }
  }

  /**
   * Get WhatsApp number for a user
   * TODO: Implement Firestore user lookup
   */
  static async getWhatsAppNumber(username: string): Promise<string | null> {
    try {
      // TODO: Replace with Firestore query
      const user = null; // Replace with Firestore query

      // TODO: Access user.whatsappNumber from Firestore document
      return null; // Replace with user?.whatsappNumber || null
    } catch (error) {
      console.error('Error getting WhatsApp number:', error);
      return null;
    }
  }
}
