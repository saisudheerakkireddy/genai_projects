import { NextRequest, NextResponse } from "next/server"

export const runtime = "edge"

const PY_BACKEND_URL = process.env.PY_BACKEND_URL || 'http://localhost:5000';
const ROBOFLOW_URL = 'https://serverless.roboflow.com/care-connect/workflows/custom-workflow-2'
const ROBOFLOW_API_KEY = (typeof process !== 'undefined' && (process as any).env && (process as any).env.ROBOFLOW_API_KEY) ? (process as any).env.ROBOFLOW_API_KEY : '6H9EKiWhrtiIpFL1T2qc'

export async function POST(req: NextRequest) {
  try {
    console.log('[analyze-xray] Incoming request')
    const formData = await req.formData()
    const file = formData.get("file") as File | null
    if (!file) {
      console.log('[analyze-xray] No file uploaded')
      return NextResponse.json({ error: "No file uploaded" }, { status: 400 })
    }
    console.log('[analyze-xray] File received:', file.name)

    // Read file into base64 for Roboflow
    const arrayBuffer = await file.arrayBuffer()
    const uint8 = new Uint8Array(arrayBuffer)
    let binary = ''
    for (let i = 0; i < uint8.length; i++) {
      binary += String.fromCharCode(uint8[i])
    }
    const base64 = btoa(binary)
    const dataUrl = `data:${file.type};base64,${base64}`

    // Call Roboflow serverless workflow
    console.log('[analyze-xray] Sending image to Roboflow')
    const rfResp = await fetch(ROBOFLOW_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        api_key: ROBOFLOW_API_KEY,
        inputs: {
          image: { type: 'base64', value: dataUrl }
        }
      })
    })
    const rfData = await rfResp.json().catch(() => null)
    console.log('[analyze-xray] Roboflow response:', rfData)

    // Prepare form data for Flask backend: include original file + Roboflow result
    const flaskForm = new FormData()
    flaskForm.append("file", file, file.name)
    if (rfData) {
      flaskForm.append('roboflow_result', JSON.stringify(rfData))
    }

    console.log('[analyze-xray] Sending to Flask backend:', `${PY_BACKEND_URL}/analyze-xray`)
    const flaskRes = await fetch(`${PY_BACKEND_URL}/analyze-xray`, {
      method: "POST",
      body: flaskForm,
    })

    console.log('[analyze-xray] Flask response status:', flaskRes.status)
    const data = await flaskRes.json().catch(() => null)
    console.log('[analyze-xray] Flask response data:', data)

    // Return combined result to frontend: include Roboflow and backend analysis
    return NextResponse.json({
      success: true,
      roboflow: rfData,
      backend: data
    }, { status: flaskRes.status || 200 })
  } catch (err) {
    console.error('[analyze-xray] Error:', err)
    return NextResponse.json({ error: 'Internal server error', details: String(err) }, { status: 500 })
  }
}