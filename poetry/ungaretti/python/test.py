"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.

Zahlenspiel is a numbers game in German.

"""

def test_json1():
    return {
	"version": "1.0",
	"session": {
		"new": "false",
		"sessionId": "amzn1.echo-api.session.868d3be3-0ac8-411a-a66c-a36f8e8356d2",
		"application": {
			"applicationId": "amzn1.ask.skill.8e31f062-4c43-474b-ac55-efa8677f2e3e"
		},
		"user": {
			"userId": "amzn1.ask.account.AFQ2JEKK7NY57ZXUDRRKNNFH5SBZGZUFYYEW54WIE6TD2SIFP5X5W6SSTER2P6GX4DDXSIZ324WL3GMRRB5FEUKJJI3D5CEW2VVX35UHIVJWBV4O2TRVPX35X7AKMA6SKD5OEPKRVKY66YU3QMHBGMH33YEHSG325RA5STTAKYU3AYWEDKYFHD7FQBLLT4WFPPPAKZXX5M3FPXY"
		}
	},
	"context": {
		"System": {
			"application": {
				"applicationId": "amzn1.ask.skill.8e31f062-4c43-474b-ac55-efa8677f2e3e"
			},
			"user": {
				"userId": "amzn1.ask.account.AFQ2JEKK7NY57ZXUDRRKNNFH5SBZGZUFYYEW54WIE6TD2SIFP5X5W6SSTER2P6GX4DDXSIZ324WL3GMRRB5FEUKJJI3D5CEW2VVX35UHIVJWBV4O2TRVPX35X7AKMA6SKD5OEPKRVKY66YU3QMHBGMH33YEHSG325RA5STTAKYU3AYWEDKYFHD7FQBLLT4WFPPPAKZXX5M3FPXY"
			},
			"device": {
				"deviceId": "amzn1.ask.device.AFW3JIPGHWGAAFUMMEB42MMQY6MFE5TO2FJJQSB6OTOCDOUCEUY4OGRPMSGN3F3XZECEQ6O3WKSXTY6LYHCRCSNQCQ5PRXLG3HEDY7FLDL2AOOUASHSHBSZJ77X2EAJMRFU4BN3CDZVZCG24HD4HNKXZYYAQ",
				"supportedInterfaces": {}
			},
			"apiEndpoint": "https://api.amazonalexa.com",
			"apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjhlMzFmMDYyLTRjNDMtNDc0Yi1hYzU1LWVmYTg2NzdmMmUzZSIsImV4cCI6MTUzMzgxMzA1NiwiaWF0IjoxNTMzODA5NDU2LCJuYmYiOjE1MzM4MDk0NTYsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUZXM0pJUEdIV0dBQUZVTU1FQjQyTU1RWTZNRkU1VE8yRkpKUVNCNk9UT0NET1VDRVVZNE9HUlBNU0dOM0YzWFpFQ0VRNk8zV0tTWFRZNkxZSENSQ1NOUUNRNVBSWExHM0hFRFk3RkxETDJBT09VQVNIU0hCU1pKNzdYMkVBSk1SRlU0Qk4zQ0RaVlpDRzI0SEQ0SE5LWFpZWUFRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUZRMkpFS0s3Tlk1N1pYVURSUktOTkZINVNCWkdaVUZZWUVXNTRXSUU2VEQyU0lGUDVYNVc2U1NURVIyUDZHWDRERFhTSVozMjRXTDNHTVJSQjVGRVVLSkpJM0Q1Q0VXMlZWWDM1VUhJVkpXQlY0TzJUUlZQWDM1WDdBS01BNlNLRDVPRVBLUlZLWTY2WVUzUU1IQkdNSDMzWUVIU0czMjVSQTVTVFRBS1lVM0FZV0VES1lGSEQ3RlFCTExUNFdGUFBQQUtaWFg1TTNGUFhZIn19.GYgY7ZXh4atu3zVo1kd20rSlQPBabaYdEd6r66cGpv0RTQaubbgtf98REBye4gKyyHuVrHdkpnsJuf4zdTHE00BwjLz8bfDJV1nI1SR_tAj-S43CKSRd4j-mWxHpUjGeAV3ZSc2ORMG0sSZjghjNiY8OI8JOTjZLP6twfEMDJuR6ZCOuzqxx2T3CV2PMeGjZbMGrQ1cswvn5NHQz1tKq2rPNhcezU2VbI3Pyc275fZqGRUbqja1DxvqHqTHyhfOYwrnvGhUZa5nVaQi1Kp9k3YPzeDv-6DJiyJpyTZrkM1O_KffC4V6CHI1W2x4gdL8iyByt7Qt0GnxA91LO_IkiBg"
		}
	},
	"request": {
		"type": "IntentRequest",
		"requestId": "amzn1.echo-api.request.3408217d-3918-4c0f-a556-bfa56cfe3be0",
		"timestamp": "2018-08-09T10:10:56Z",
		"locale": "en-GB",
		"intent": {
			"name": "GetCanonicalIntent",
			"confirmationStatus": "NONE",
			"slots": {
				"canonical": {
					"name": "canonical",
					"value": "Spanish",
					"resolutions": {
						"resolutionsPerAuthority": [
							{
								"authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.8e31f062-4c43-474b-ac55-efa8677f2e3e.CANONICALS_LIST",
								"status": {
									"code": "ER_SUCCESS_MATCH"
								},
								"values": [
									{
										"value": {
											"name": "spanish",
											"id": "canonical_93"
										}
									}
								]
							}
						]
					},
					"confirmationStatus": "NONE"
				}
			}
		}
	}
     }
