# for api calls
import requests, json
# from requests.auth import HTTPBasicAuth

# pyodbc is used for connecting to the database
import pyodbc

# # INITIALIZE SQL STUFF
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DCIDS-SQL-DEV1;'
    'Database=DCIDSDW;'
    'Trusted_Connection=yes;'
    )
# initialize cursor
cursor = conn.cursor()

# build select statement
# selectSourceFileIds = f"SELECT AFO.[Id], ORG.[OwnedByOrganizationName], AFO.[SourceFileName], ORG.[OrganizationName]	FROM	[iTxRepl].[dbo].[AttachmentForOrganization] AFO	INNER JOIN [DCIDSDW].[Dim].[Organization] ORG ON ORG.[OrganizationId] = AFO.[OrganizationId]WHERE	ORG.[IsActive] = 'Yes'	AND ORG.[IsHospital] = 'Yes'	AND AFO.[SourceFileName] LIKE '%SOA%'	AND AFO.[SourceFileName] NOT LIKE '%TX%'	AND ORG.[OrganizationName] LIKE '%University of California Davis Medical Center%'	AND AFO.[SourceFileName] LIKE '%UC Davis - SOA 2018.pdf%' ORDER BY	ORG.[OwnedByOrganizationName]	, ORG.[OrganizationName]"
selectSourceFileIds = f"SELECT AFO.[Id], ORG.[OwnedByOrganizationName], AFO.[SourceFileName], ORG.[OrganizationName] FROM [iTxRepl].[dbo].[AttachmentForOrganization] AFO INNER JOIN [DCIDSDW].[Dim].[Organization] ORG ON ORG.[OrganizationId] = AFO.[OrganizationId] WHERE 	ORG.[IsActive] = 'Yes' 	AND ORG.[IsHospital] = 'Yes' AND (AFO.[SourceFileName] LIKE '%SOA%'		OR AFO.[Description] LIKE '%SOA%'		OR AFO.[SourceFileName] LIKE '%Agreement%'		AND AFO.[SourceFileName] NOT LIKE '%TX%') ORDER BY 	ORG.[OwnedByOrganizationName] 	, ORG.[OrganizationName]"
#execute the sql statement
sourceFileIds = cursor.execute(selectSourceFileIds)
# get all rows from the sql return value
sourceFileIds = sourceFileIds.fetchall()

def main():

    for sourceFileId in sourceFileIds:
        fileId = sourceFileId[0]
        OPO = sourceFileId[1]
        sourceFileName = sourceFileId[2]
        organizationName = sourceFileId[3]
        
        # build the string to request the attachment
        attachmentRequestString = f"https://dcids.itransplant.net/WebUI/Base.mvc/Attachment/DownloadOrganizationAttachment?attId={fileId}"

        headers = {
                'authority' : 'dcids.itransplant.net'
            , 'method': 'GET'
            , 'path': f'/WebUI/Base.mvc/Attachment/DownloadOrganizationAttachment?attId={fileId}'
            , 'scheme' : 'https'
            , 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            , 'accept-encoding' : 'gzip, deflate, br'
            , 'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"'
            , 'sec-fetch-dest' : 'document'
            , 'sec-fetch-mode' : 'navigate'
            ,'sec-fetch-site' : 'same-origin'

                # NOTE  I think you need to replace this cookie for this to work
            ,'cookie' : 'FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U2VjdXJpdHlDb250ZXh0VG9rZW4gcDE6SWQ9Il8yODU1YjQ1NC04MmFkLTQ3ODQtOTZmYi0wNWU4NWQ4MzBiOTgtRjg4MTVFOUM5MjBBNDBDNDhCRERDRjQ5ODMyQzUzMTAiIHhtbG5zOnAxPSJodHRwOi8vZG9jcy5vYXNpcy1vcGVuLm9yZy93c3MvMjAwNC8wMS9vYXNpcy0yMDA0MDEtd3NzLXdzc2VjdXJpdHktdXRpbGl0eS0xLjAueHNkIiB4bWxucz0iaHR0cDovL2RvY3Mub2FzaXMtb3Blbi5vcmcvd3Mtc3gvd3Mtc2VjdXJlY29udmVyc2F0aW9uLzIwMDUxMiI+PElkZW50aWZpZXI+dXJuOnV1aWQ6YjA3M2MwYTgtMDBkMS00OTE0LTgxNGMtNmVkOWVhYjg1MzA3PC9JZGVudGlmaWVyPjwvU2VjdXJpdHlDb250ZXh0VG9rZW4+; ASP.NET_SessionId=rckyzlmorz2rnr4kqgrhzn1g; TC_ASPXFORMSAUTH=25B4923E7AA2D2CCD3E7AA319D524E9F8505BBD78DC1687E8FA404607E2F8104E7D02F0FB61F8075B3248757C83D6C1072600E7222495B0A6A4D85C7399E9B3086B76CB8C9364FA0DE72A95E7DFFCA47EF90BB6A1E644EDE8E6443B3097B6D6B3191E276EAA5C234E165D9940306500B2871EB15968F1379B4A4EE45758BCFC47642C3FDFEFD3AA98D6D3AF5657087A4E9DFCED30F8718FF35B70179050105ADAAD86D13B288C20725A718D7F4AC8F8B728ED4CAFE7B18A4207996CB9EFCC3A7215D2FE2D397188CF0C83FE7C4DA021EED2D4DE098575D1401A44EDFF278985D31A749B6869048C4148EA4BFE763FEDBD8BA3156EFDF2E16EFDE8969FFE86C9EEAF2E2338FF3A9C01CFA66E7319D1D6D5C0420E621A656AD901F938DFC4892C1A7291F644935061251E4542CA601F4D6CE01AD6AACEE255E079CA193DE7D3CC53D4FC2D59EA0C3F1C16DA90F4B649FB42ACE3D25C8FFB1B3BA69A18C8D7A7CCACA907937F12014319EB9FB53F51267766DD56D27B159F893E5C6A4F764050D4B033CE00074D1C4C7733BED60096B13D266008CDC0050F73115EB15B2E28F2849B2816D7F6D510FDBEC339D57D452CBE56B997999C32695B7DD71A395E622E64AA89F2C02F2C8CCB2ACC79AAC09E58A236210151D2A2A897021DDBF258F27D99E31528A59EAB703952566BF8918C3639A24672E419A85A8A70E87EB09D66F3B78880D263C0425EFA85A07D4533B5F9FD61C31F507EAD71AED91120633E6F9ADCECF8C64121358E31E9A1CDE1542829340ADF7886CD98F969CC94A26065F62FEE65D8BDF643D42E0D64A6FAA0246C6355624646ED024218C8F8DB71729F9B5224FD50B06E854772B1B625AA8804D40F208E54240D466FB907CED24E76F03AD5552A789A23E826B264BF1B34424AF35134D9526BFA8118B66B0526487D3381A9BBC2EC079E343C999C88A8484018201B0A3C3C2C5BD67DF5A4BAF9DC03C9B56CC9B6FD6B20E1A239F04738829CFCC1A0F464960810FBAA46AABE0A5C2F66845D5D1DCEA9BD8CFE882029A91C0699DF7CB104DEFF87A1188FDA8550D8A8B0CE49F586D4D3B7117A2BD0C54E9C3459532D9FE100B3733007160B833865AC0059FA3E53CC170E51D35906DF74FC7CAD7C602629F6AAA46919C5D0B0480C24AFC2CC8D3222E0A92A5F538B6BD5B4A452EE7DCBBA7536B781A686C6D0B88AC0115B55788807D55F00081279A97D699EA3727E273524AC1598953B3DD50395CF88A17D81EDEBFD4CF7161139D3A92231C8377060B317F520C4E65D98D935E1540348DD59699B7E8F9DC055F64FA6F446FFAFFB6BBA341CF95CB3380643E3BF6AB20CA7A3E5E0E5A39253816255813C271A92B1892E0F2F587DDF656DE42D7152B8842EA65833D0D073556A81C3ACBFD7B83C8E1A8CCBDA68476E3EDFB2315BE6223526B84310771016D4E97D868AE4DA09820D5C7C784E2BB1436BE700CA63C671C700BC21513C3C5CCEBD954BEB282D93A587D788E20AE692A9896A9C47869E1D0D2F34BE83484B4FA8E6853CFE7BCC13B68BC9E34B35141DAF9426A26E311588DEF92CD0503E24E722AF57551F6DEAC018C9373EDD92267452ABC28A4AEEF37F88F516FF41D6AF776A3D10CD53291CD9398806C68D2EEEF2F70C53457EE5012E8D34ABACCABE3413B4D2DD2A77193B09E599BC9D8B9BC7324386952AC2E72D5AC5E10210B93E5E38C287120549EDBE510AED1DF4BBB3242AC5EB13F32284E59890C5012FD805323DED2059FB7D51A3561960952; enc-dict-key={"alg":"A256CBC","ext":true,"k":"9GuTqQXIMiWVQheztRIcw6YYg-etQoIptB3yeeYb6Ss","key_ops":["encrypt","decrypt"],"kty":"oct"}'

        }
    
        saveToPath = (r'c:\Users\paul.davis\Desktop\TEST')+(f'\{OPO}\{organizationName} {sourceFileName}')
        print(saveToPath)
        downloadFile(attachmentRequestString, headers, saveToPath)


def downloadFile(downloadUrl, headers, saveToPath):
    #response = requests.get(attachmentRequestString, allow_redirects=True, auth=HTTPBasicAuth('paul.davis@dcids.org', 'Fuzzy.Kittens5'), headers=headers )
    response = requests.get(downloadUrl, allow_redirects=True, headers=headers )
    # time.sleep(3)

    content = response.content
    open(saveToPath, 'wb').write(content)

    print("completed")
    print(response.status_code)
    # responseHeaders = response.headers
    # print(responseHeaders)
    print(downloadUrl)

main()



