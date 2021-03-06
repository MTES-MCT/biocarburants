import { ApiState } from "common/hooks/use-api"
import { Certificate } from "common/types"
import { CertificateSettings } from "settings/components/certificates"

type CertificatesProps = {
  certificates: ApiState<Certificate[]>
}

const Certificates = ({ certificates }: CertificatesProps) => {
  return (
    <CertificateSettings
      loading={certificates.loading}
      type="2BS & ISCC & REDcert & SN"
      certificates={certificates.data ?? []}
    />
  )
}

export default Certificates
