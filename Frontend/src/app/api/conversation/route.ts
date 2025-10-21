import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, conversationId, resetConversation = false } = body;

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    // Call the Python conversation agent server
    const response = await fetch('http://localhost:5001/api/agent/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message,
        reset_conversation: resetConversation,
      }),
    });

    if (!response.ok) {
      throw new Error(`Python server responded with status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Agent response data:', data);
    console.log('Data type:', typeof data);
    console.log('Data keys:', Object.keys(data));
    console.log('Main response exists:', !!data.main_response);
    console.log('Profiles exists:', !!data.profiles);
    console.log('Profiles length:', data.profiles ? data.profiles.length : 'N/A');

    // Format the response for the chat interface
    let aiResponse = '';

    if (data.main_response) {
      aiResponse = data.main_response;
      console.log('Using main_response as AI response');
    } else {
      aiResponse = "I couldn't process your request properly.";
      console.log('No main_response found, using fallback');
    }

    const finalResponse = {
      response: aiResponse,
      profiles: data.profiles || []
    };
    
    console.log('Final API response:', finalResponse);
    return NextResponse.json(finalResponse);

  } catch (error) {
    console.error('Error calling conversation agent:', error);

    // Fallback response
    return NextResponse.json({
      response: "I'm sorry, I'm having trouble connecting to the candidate database right now. Please try again in a moment.",
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}