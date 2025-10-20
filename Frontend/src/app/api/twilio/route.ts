import { NextRequest, NextResponse } from 'next/server';
import { Twilio } from 'twilio';

const twilioClient = new Twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);
const twilioWhatsAppNumber = process.env.TWILIO_WHATSAPP_NUMBER;

/**
 * Send WhatsApp message via Twilio
 */
export async function sendWhatsAppMessage(
  to: string,
  body: string
): Promise<void> {
  try {
    if (!twilioWhatsAppNumber) {
      throw new Error('TWILIO_WHATSAPP_NUMBER environment variable is not set');
    }

    if (!to) {
      throw new Error('Recipient number is empty');
    }

    if (!body) {
      throw new Error('Message body is empty');
    }

    const message = await twilioClient.messages.create({
      from: twilioWhatsAppNumber,
      to: to,
      body: body,
    });

    console.log(`[WhatsApp] Message sent successfully: ${message.sid}`);
  } catch (error: any) {
    console.error('[WhatsApp Send] Error:', error);
    console.error('[WhatsApp Send] Error Code:', error.code || 'unknown');
    console.error('[WhatsApp Send] Error Message:', error.message || 'unknown');
    throw error;
  }
}

/**
 * POST endpoint to handle incoming WhatsApp messages from Twilio webhook
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.formData();
    const from = body.get('From') as string;
    const message = (body.get('Body') as string || '').trim();
    const numMedia = parseInt(body.get('NumMedia') as string || '0');

    if (!from) {
      return new NextResponse('Missing From field', { status: 400 });
    }

    const whatsappNumber = from.replace('whatsapp:', '');

    console.log('[WhatsApp Inbound]', {
      from: whatsappNumber,
      message,
      hasMedia: numMedia > 0,
    });

    // TODO: Implement Firestore user lookup
    // Check if user exists with this WhatsApp number
    const user = null; // Replace with Firestore query

    if (!user) {
      // Handle account linking
      const tokenMatch = message.match(/[a-fA-F0-9]{64}/);
      const token = tokenMatch ? tokenMatch[0] : null;

      if (!token) {
        await sendWhatsAppMessage(
          from,
          '❌ No valid token found. Please generate a token from your user profile and send it here to link your account.'
        );
        return new NextResponse(null, { status: 204 });
      }

      // TODO: Implement Firestore user lookup by token
      const userToLink = null; // Replace with Firestore query

      if (userToLink) {
        // TODO: Implement Firestore user update
        // Update user with whatsappNumber and clear whatsappKey

        await sendWhatsAppMessage(
          from,
          `✅ Your WhatsApp is now linked!\n\nYou can now receive messages from the system.`
        );
      } else {
        await sendWhatsAppMessage(
          from,
          '❌ Invalid token. Please generate a new token from your user profile and try again.'
        );
      }

      return new NextResponse(null, { status: 204 });
    }

    // User exists - echo back the message for now
    await sendWhatsAppMessage(
      from,
      `Message received: "${message}"\n\nYour account is linked.`
    );

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    console.error('[WhatsApp] Error processing webhook:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
